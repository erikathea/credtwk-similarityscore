package main

import (
	"encoding/csv"
	"flag"
	"fmt"
	"log"
	"math"
	"os"
	"strconv"
	"strings"

	"github.com/hbollon/go-edlib"
)

func main() {
	inputFile := flag.String("csv", "", "Path to the input CSV file containing password data")   // Input CSV with header: variant1,variant2,...,variant10, pw1, total_duration
	outputFile := flag.String("output", "computed.csv", "Path to the output CSV file")// Output CSV with header: pw1, num_variants, average_case_sensitive_hss, average_case_insensitive_hss, total_duration
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
	requiredColumns := []string{"pw1", "total_duration"}
	for i := 1; i <= 10; i++ {
		requiredColumns = append(requiredColumns, fmt.Sprintf("variant%d", i))
	}
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
	// Write header for the computed CSV.
	outputHeader := []string{"pw1", "num_variants", "average_case_sensitive_hss", "average_case_insensitive_hss", "total_duration"}
	if err := writer.Write(outputHeader); err != nil {
		log.Fatalf("Error writing header to CSV: %v", err)
	}

	for rowIndex, row := range records[1:] {
		pw1 := row[colIndex["pw1"]]
		totalDuration := row[colIndex["total_duration"]]

		var sumCaseSensitive, sumCaseInsensitive float64
		var countVariants int

		fmt.Printf("Processing row %d: pw1 = %s, total_duration = %s\n", rowIndex+1, pw1, totalDuration)

		for i := 1; i <= 10; i++ {
			colName := fmt.Sprintf("variant%d", i)
			variant := strings.TrimSpace(row[colIndex[colName]])
			if variant != "" {
				countVariants++
				cs := hybridSimilarity(pw1, variant, 0.5, 0.5)
				ci := hybridSimilarity(strings.ToLower(pw1), strings.ToLower(variant), 0.5, 0.5)
				sumCaseSensitive += cs
				sumCaseInsensitive += ci
			}
		}

		var avgCaseSensitive, avgCaseInsensitive float64
		if countVariants > 0 {
			avgCaseSensitive = sumCaseSensitive / float64(countVariants)
			avgCaseInsensitive = sumCaseInsensitive / float64(countVariants)
		}

		fmt.Printf("Row %d computed: num_variants = %d, avg_case_sensitive_hss = %.4f, avg_case_insensitive_hss = %.4f\n",
			rowIndex+1, countVariants, avgCaseSensitive, avgCaseInsensitive)
		// Write the computed row to the output CSV.
		outputRecord := []string{
			pw1,
			strconv.Itoa(countVariants),
			fmt.Sprintf("%.4f", avgCaseSensitive),
			fmt.Sprintf("%.4f", avgCaseInsensitive),
			totalDuration,
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
