package main

import (
    "bytes"
    "encoding/csv"
    "encoding/json"
    "flag"
    "fmt"
    "github.com/hbollon/go-edlib"
    "io/ioutil"
    "log"
    "math"
    "net/http"
    "os"
    //"regexp"
    "strconv"
    "strings"
)

// GenerateRequest defines the payload sent to Ollama.
type GenerateRequest struct {
    Model  string `json:"model"`
    Prompt string `json:"prompt"`
    Stream bool   `json:"stream"`
}

// GenerateResponse represents the JSON structure returned by Ollama.
type GenerateResponse struct {
    Model              string `json:"model"`
    CreatedAt          string `json:"created_at"`
    Response           string `json:"response"`
    TotalDuration      int64  `json:"total_duration"`
    LoadDuration       int64  `json:"load_duration"`
    PromptEvalCount    int    `json:"prompt_eval_count"`
    PromptEvalDuration int64  `json:"prompt_eval_duration"`
    EvalCount          int    `json:"eval_count"`
    EvalDuration       int64  `json:"eval_duration"`
}

func extractVariants(generatedText string, numVariants int) []string {
    // Remove chain-of-thought if present.
    if strings.Contains(generatedText, "</think>") {
        parts := strings.SplitN(generatedText, "</think>", 2)
        if len(parts) > 1 {
            generatedText = parts[1]
        }
    }

    lines := strings.Split(generatedText, "\n")
    var variants []string

    for _, line := range lines {
        trimmed := strings.TrimSpace(line)

        // Skip empty lines and unwanted headers
        if trimmed == "" || strings.HasPrefix(trimmed, "Wait,") || strings.HasPrefix(trimmed, "Here") || strings.HasPrefix(trimmed, "I think") {
            continue
        }

        // If line starts with a number (e.g., "1. password1"), remove the prefix
        parts := strings.Fields(trimmed)
        if len(parts) > 1 && strings.HasSuffix(parts[0], ".") { // Checks if first word is like "1."
            trimmed = strings.Join(parts[1:], " ") // Remove numbering
        }

        variants = append(variants, trimmed)
        if len(variants) == numVariants {
            break
        }
    }
    return variants
}

func hybridSimilarity(str1, str2 string, w1, w2 float64) float64 {
    freqSimilarity := customCosineSimilarity(str1, str2)
    orderSimilarity := damerauLevenshteinSimilarity(str1, str2)
    return (w1 * freqSimilarity) + (w2 * orderSimilarity)
}

func damerauLevenshteinSimilarity(str1, str2 string) float64 {
    score, _ := edlib.StringsSimilarity(str1, str2, edlib.OSADamerauLevenshtein)
    return float64(score)
}

func customCosineSimilarity(str1, str2 string) float64 {
    charSet := make(map[rune]bool)
    for _, ch := range str1 {
        charSet[ch] = true
    }
    for _, ch := range str2 {
        charSet[ch] = true
    }

    charIndex := make(map[rune]int)
    index := 0
    for ch := range charSet {
        charIndex[ch] = index
        index++
    }

    vectorSize := len(charSet)
    vector1 := make([]float64, vectorSize)
    vector2 := make([]float64, vectorSize)

    for _, ch := range str1 {
        idx := charIndex[ch]
        vector1[idx]++
    }

    for _, ch := range str2 {
        idx := charIndex[ch]
        vector2[idx]++
    }

    dotProduct := 0.0
    magnitude1 := 0.0
    magnitude2 := 0.0

    for i := 0; i < vectorSize; i++ {
        dotProduct += vector1[i] * vector2[i]
        magnitude1 += vector1[i] * vector1[i]
        magnitude2 += vector2[i] * vector2[i]
    }

    if magnitude1 == 0 || magnitude2 == 0 {
        return 0.0
    }

    return dotProduct / (math.Sqrt(magnitude1) * math.Sqrt(magnitude2))
}

func writeCSV(rows [][]string, outputFilePath string, header []string, headerWritten bool) (bool, error) {
    file, err := os.OpenFile(outputFilePath, os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0644)
    if err != nil {
        return headerWritten, fmt.Errorf("error opening output file: %v", err)
    }
    defer file.Close()

    writer := csv.NewWriter(file)
    if !headerWritten {
        if err := writer.Write(header); err != nil {
            return headerWritten, fmt.Errorf("error writing header: %v", err)
        }
        headerWritten = true
    }
    for _, row := range rows {
    if err := writer.Write(row); err != nil {
            return headerWritten, fmt.Errorf("error writing row: %v", err)
        }
    }
    writer.Flush()
    if err := writer.Error(); err != nil {
        return headerWritten, fmt.Errorf("error flushing writer: %v", err)
    }
    return headerWritten, nil
}

func main() {
    modelName := flag.String("model", "", "Model name to use for generating password variants")
    csvFilePath := flag.String("csv", "", "Path to the input CSV file containing password data")
    outputFilePath := flag.String("output", "output.csv", "Path to the output CSV file")
    promptTemplate := flag.Int("prompt", 1, "Select prompt template for generating password variants (1,2,3)")
    numVariants := flag.Int("variants", 10, "Number of password variants to generate")
    flag.Parse()

    log.Printf("promptTemplate %d \n numVariants: %d", *promptTemplate, *numVariants)
    if *modelName == "" || *csvFilePath == "" {
        flag.Usage()
        os.Exit(1)
    }

    inputFile, err := os.Open(*csvFilePath)
    if err != nil {
        log.Fatalf("Error opening input CSV file: %v", err)
    }
    defer inputFile.Close()

    csvReader := csv.NewReader(inputFile)
    records, err := csvReader.ReadAll()
    if err != nil {
        log.Fatalf("Error reading CSV file: %v", err)
    }
    if len(records) < 1 {
        log.Fatalf("CSV file is empty")
    }

    blocklistFile, err := os.OpenFile("password_tweaks_blocklist", os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0644)
    if err != nil {
        log.Fatalf("Error opening blocklist file: %v", err)
    }
    defer blocklistFile.Close()
    var blocklistBuffer bytes.Buffer
    blocklistThreshold := 5
    blocklistCount := 0

    header := records[0]
    var usernameIndex, pw1Index, pw2Index int = -1, -1, -1
    for i, h := range header {
        switch strings.TrimSpace(h) {
        case "username":
            usernameIndex = i
        case "pw1":
            pw1Index = i
        case "pw2":
            pw2Index = i
        }
    }
    if pw1Index == -1 {
        log.Fatalf("CSV header must contain 'password' column")
    }
    if (*promptTemplate == 2 || *promptTemplate == 3) && pw2Index == -1 {
        log.Fatalf("CSV header must contain 'password2' column for prompt type %d", *promptTemplate)
    }
    if *promptTemplate == 3 && usernameIndex == -1 {
        log.Fatalf("CSV header must contain 'username' column for prompt type 3")
    }

    outputHeader := []string{"username", "pw1", "pw2"}
    for i := 1; i <= *numVariants; i++ {
        outputHeader = append(outputHeader, fmt.Sprintf("variant%d", i))
        outputHeader = append(outputHeader, fmt.Sprintf("cs_hss_pw1_%d", i))
        outputHeader = append(outputHeader, fmt.Sprintf("ci_hss_pw1_%d", i))
        outputHeader = append(outputHeader, fmt.Sprintf("cs_hss_pw2_%d", i))
        outputHeader = append(outputHeader, fmt.Sprintf("ci_hss_pw2_%d", i))
        outputHeader = append(outputHeader, fmt.Sprintf("cs_hss_user_%d", i))
        outputHeader = append(outputHeader, fmt.Sprintf("ci_hss_user_%d", i))
    }
    outputHeader = append(outputHeader, "total_duration", "load_duration", "prompt_eval_count",
    "prompt_eval_duration", "eval_count", "eval_duration")

    var outputRows [][]string
    headerWritten := false
    autoSaveThreshold := 5
    fixedInstructions := " The result must be different from the base password. Each result must be at least 8 characters long. List each variant on a new line with no extra text, numbering, or formatting. Do not include any internal reasoning or chain-of-thought. Output only the results.<｜Assistant｜>"

    for i, record := range records[1:] {
        if len(record) <= pw1Index {
            log.Printf("Skipping row %d: not enough columns", i+2)
            continue
        }
        username := record[usernameIndex]
        pw1 := record[pw1Index]
        pw2 := record[pw2Index]

        var prompt string
        switch *promptTemplate {
        case 1:
            prompt = fmt.Sprintf(`<｜User｜>Please generate %d password variants from "%s".`, *numVariants, pw1)
        case 2:
            prompt = fmt.Sprintf(`<｜User｜>Please generate %d password variants for the breached passwords "%s", "%s".`, *numVariants, pw1, pw2)
        case 3:
            prompt = fmt.Sprintf(`<｜User｜>Please generate %d password variants for the breached passwords "%s", "%s" with username "%s".`, *numVariants, pw1, pw2, username)
        }
        prompt += fixedInstructions

        reqPayload := GenerateRequest{
            Model:  *modelName,
            Prompt: prompt,
            Stream: false,
        }
        jsonData, err := json.Marshal(reqPayload)
        if err != nil {
            log.Printf("Error marshalling JSON for row %d: %v", i+2, err)
            continue
        }

        // Send POST request to Ollama.
        url := "http://localhost:11434/api/generate"
        resp, err := http.Post(url, "application/json", bytes.NewBuffer(jsonData))
        if err != nil {
            log.Printf("Error sending request for row %d: %v", i+2, err)
            continue
        }
        responseBody, err := ioutil.ReadAll(resp.Body)
        resp.Body.Close()
        if err != nil {
            log.Printf("Error reading response for row %d: %v", i+2, err)
            continue
        }
        if resp.StatusCode != http.StatusOK {
            log.Printf("Non-OK HTTP status for row %d: %d - %s", i+2, resp.StatusCode, string(responseBody))
            continue
        }

        var genResp GenerateResponse
        err = json.Unmarshal(responseBody, &genResp)
        if err != nil {
            log.Printf("Error unmarshalling JSON for row %d: %v", i+2, err)
            continue
        }

        // Print the full "response" block for assessment.
        //log.Printf("--------Row %d: Raw model response:\n%s", i+2, genResp.Response)

        // Extract the password variants.
        variants := extractVariants(genResp.Response, *numVariants)
        if variants == nil || len(variants) < *numVariants {
            log.Printf("Row %d: Expected %d variants, got %d", i+2, *numVariants, len(variants))
            for len(variants) < *numVariants {
                variants = append(variants, "")
            }
        } else if len(variants) > *numVariants {
            variants = variants[:*numVariants]
        }

        row := []string{
            username,
            pw1,
            pw2,
        }

        for _, variant := range variants {
            row = append(row, variant)
            cs_hss_pw1 := hybridSimilarity(pw1, variant, 0.5, 0.5)
            row = append(row, fmt.Sprintf("%.4f", cs_hss_pw1))

            ci_hss_pw1 := hybridSimilarity(strings.ToLower(pw1), strings.ToLower(variant), 0.5, 0.5)
            row = append(row, fmt.Sprintf("%.4f", ci_hss_pw1))

            cs_hss_pw2 := hybridSimilarity(pw2, variant, 0.5, 0.5)
            row = append(row, fmt.Sprintf("%.4f", cs_hss_pw2))

            ci_hss_pw2 := hybridSimilarity(strings.ToLower(pw2), strings.ToLower(variant), 0.5, 0.5)
            row = append(row, fmt.Sprintf("%.4f", ci_hss_pw2))

            cs_hss_user := hybridSimilarity(username, variant, 0.5, 0.5)
            row = append(row, fmt.Sprintf("%.4f", cs_hss_user))

            ci_hss_user := hybridSimilarity(strings.ToLower(username), strings.ToLower(variant), 0.5, 0.5)
            row = append(row, fmt.Sprintf("%.4f", ci_hss_user))
        }
        row = append(row,
            strconv.FormatInt(genResp.TotalDuration, 10),
            strconv.FormatInt(genResp.LoadDuration, 10),
            strconv.Itoa(genResp.PromptEvalCount),
            strconv.FormatInt(genResp.PromptEvalDuration, 10),
            strconv.Itoa(genResp.EvalCount),
            strconv.FormatInt(genResp.EvalDuration, 10),
        )
        outputRows = append(outputRows, row)
        /*outputHeader = append(outputHeader, 
            "avg_cs_hss_pw1", 
            "avg_ci_hss_pw1", 
            "avg_cs_hss_pw2", 
            "avg_ci_hss_pw2", 
            "avg_cs_hss_user", 
            "avg_ci_hss_user"
        )*/

        // Auto-save
        if blocklistCount >= blocklistThreshold {
            _, err := blocklistFile.Write(blocklistBuffer.Bytes())
            if err != nil {
                log.Printf("Error writing to blocklist file: %v", err)
            } else {
                log.Printf("Auto-saved %d entries to blocklist", blocklistCount)
            }
            blocklistBuffer.Reset()
            blocklistCount = 0
        }
        if len(outputRows) >= autoSaveThreshold {
            headerWritten, err = writeCSV(outputRows, *outputFilePath, outputHeader, headerWritten)
            if err != nil {
                log.Printf("Error writing output CSV: %v", err)
            } else {
                log.Printf("Auto-saved %d rows up to input row %d", len(outputRows), i+2)
            }
            outputRows = [][]string{}
        }
    }

    if blocklistBuffer.Len() > 0 {
        _, err := blocklistFile.Write(blocklistBuffer.Bytes())
        if err != nil {
            log.Printf("Error writing final blocklist entries: %v", err)
        } else {
            log.Printf("Final save: wrote %d remaining blocklist entries", blocklistCount)
        }
    }
    if len(outputRows) > 0 {
        headerWritten, err = writeCSV(outputRows, *outputFilePath, outputHeader, headerWritten)
        if err != nil {
            log.Printf("Error writing final output CSV: %v", err)
        } else {
            log.Printf("Final save: wrote %d remaining rows", len(outputRows))
        }
    }

    log.Println("Processing complete.")
}
