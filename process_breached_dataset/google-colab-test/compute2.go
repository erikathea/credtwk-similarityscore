package main

import (
	"encoding/csv"
	"flag"
	"fmt"
	"log"
	"math"
	"os"
	//"strconv"
	"strings"

	"github.com/hbollon/go-edlib"
)

func main() {
	inputFile := flag.String("csv", "", "Path to the input CSV file containing password data (expected columns: variant1,...,variant10, username, pw1, pw2, user, total_duration)")
	outputFile := flag.String("output", "computed.csv", "Path to the output CSV file")
	flag.Parse()

	inFile, err := os.Open(*inputFile)
	if err != nil {
		log.Fatalf("Error opening input file: %v", err)
	}
	defer inFile.Close()

	reader := csv.NewReader(inFile)
	records, err := reader.ReadAll()
	if err != nil {
		log.Fatalf("Error reading CSV file: %v", err)
	}
	if len(records) < 1 {
		log.Fatalf("CSV file is empty")
	}

	header := records[0]
	colIndex := make(map[string]int)
	for i, col := range header {
		colIndex[col] = i
	}

	// Ensure required columns exist.
	requiredColumns := []string{}
	// Variant columns.
	for i := 1; i <= 10; i++ {
		requiredColumns = append(requiredColumns, fmt.Sprintf("variant%d", i))
	}
	// Additional required columns.
	requiredColumns = append(requiredColumns, "username", "pw1", "pw2", "total_duration")
	for _, col := range requiredColumns {
		if _, ok := colIndex[col]; !ok {
			log.Fatalf("Missing required column: %s", col)
		}
	}

	// Prepare the output CSV file.
	outFile, err := os.Create(*outputFile)
	if err != nil {
		log.Fatalf("Error creating output file: %v", err)
	}
	defer outFile.Close()

	writer := csv.NewWriter(outFile)
	// Write the new header for the computed CSV.
	outputHeader := []string{
		"username", "pw1", "pw2", "total_duration",
		"ave_cs_hss_pw1", "ave_ci_hss_pw1",
		"ave_cs_hss_pw2", "ave_ci_hss_pw2",
		"ave_cs_hss_user", "ave_ci_hss_user",
	}
	if err := writer.Write(outputHeader); err != nil {
		log.Fatalf("Error writing header to CSV: %v", err)
	}

	// Process each row (skipping header)
	for rowIndex, row := range records[1:] {
		username := row[colIndex["username"]]
		pw1 := row[colIndex["pw1"]]
		pw2 := row[colIndex["pw2"]]
		totalDuration := row[colIndex["total_duration"]]

		var sumCS_pw1, sumCI_pw1 float64
		var sumCS_pw2, sumCI_pw2 float64
		var sumCS_user, sumCI_user float64
		var countVariants int

		fmt.Printf("Processing row %d: username = %s, pw1 = %s, pw2 = %s\n", rowIndex+1, username, pw1, pw2)

		// Loop over each variant column.
		for i := 1; i <= 10; i++ {
			colName := fmt.Sprintf("variant%d", i)
			variant := strings.TrimSpace(row[colIndex[colName]])
			if variant != "" {
				countVariants++

				// Compute hybrid similarities for pw1.
				cs_pw1 := hybridSimilarity(pw1, variant, 0.5, 0.5)
				ci_pw1 := hybridSimilarity(strings.ToLower(pw1), strings.ToLower(variant), 0.5, 0.5)
				sumCS_pw1 += cs_pw1
				sumCI_pw1 += ci_pw1

				// Compute hybrid similarities for pw2.
				cs_pw2 := hybridSimilarity(pw2, variant, 0.5, 0.5)
				ci_pw2 := hybridSimilarity(strings.ToLower(pw2), strings.ToLower(variant), 0.5, 0.5)
				sumCS_pw2 += cs_pw2
				sumCI_pw2 += ci_pw2

				// Compute hybrid similarities for user.
				cs_user := hybridSimilarity(username, variant, 0.5, 0.5)
				ci_user := hybridSimilarity(strings.ToLower(username), strings.ToLower(variant), 0.5, 0.5)
				sumCS_user += cs_user
				sumCI_user += ci_user
			}
		}

		var avgCS_pw1, avgCI_pw1, avgCS_pw2, avgCI_pw2, avgCS_user, avgCI_user float64
		if countVariants > 0 {
			avgCS_pw1 = sumCS_pw1 / float64(countVariants)
			avgCI_pw1 = sumCI_pw1 / float64(countVariants)
			avgCS_pw2 = sumCS_pw2 / float64(countVariants)
			avgCI_pw2 = sumCI_pw2 / float64(countVariants)
			avgCS_user = sumCS_user / float64(countVariants)
			avgCI_user = sumCI_user / float64(countVariants)
		}

		fmt.Printf("Row %d computed: countVariants = %d, ave_cs_hss_pw1 = %.4f, ave_ci_hss_pw1 = %.4f, ave_cs_hss_pw2 = %.4f, ave_ci_hss_pw2 = %.4f, ave_cs_hss_user = %.4f, ave_ci_hss_user = %.4f\n",
			rowIndex+1, countVariants, avgCS_pw1, avgCI_pw1, avgCS_pw2, avgCI_pw2, avgCS_user, avgCI_user)

		outputRecord := []string{
			username,
			pw1,
			pw2,
			totalDuration,
			fmt.Sprintf("%.4f", avgCS_pw1),
			fmt.Sprintf("%.4f", avgCI_pw1),
			fmt.Sprintf("%.4f", avgCS_pw2),
			fmt.Sprintf("%.4f", avgCI_pw2),
			fmt.Sprintf("%.4f", avgCS_user),
			fmt.Sprintf("%.4f", avgCI_user),
		}
		if err := writer.Write(outputRecord); err != nil {
			log.Fatalf("Error writing record to CSV: %v", err)
		}
	}
	writer.Flush()
	if err := writer.Error(); err != nil {
		log.Fatalf("Error flushing CSV writer: %v", err)
	}

	fmt.Printf("Computed CSV file written to %s\n", *outputFile)
}

func hybridSimilarity(str1, str2 string, w1, w2 float64) float64 {
	freqSimilarity := customCosineSimilarity(str1, str2)
	orderSimilarity := damerauLevenshteinSimilarity(str1, str2)
	return (w1 * freqSimilarity) + (w2 * orderSimilarity)
}

func damerauLevenshteinSimilarity(str1, str2 string) float64 {
	score, err := edlib.StringsSimilarity(str1, str2, edlib.OSADamerauLevenshtein)
	if err != nil {
		return 0.0
	}
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
		vector1[charIndex[ch]]++
	}
	for _, ch := range str2 {
		vector2[charIndex[ch]]++
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
