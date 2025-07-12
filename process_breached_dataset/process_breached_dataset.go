package main

import (
    "bufio"
    "encoding/csv"
    "encoding/json"
    "fmt"
    "github.com/axiomhq/hyperloglog"
    "github.com/hbollon/go-edlib"
    "io/ioutil"
    "log"
    "math"
    "math/rand"
    "os"
    "path/filepath"
    "regexp"
    "sort"
    "time"
    "strings"
    "unicode"
    "unicode/utf8"    
)
const (
    commonDelimiter     = ";"   // semicolons separator
    passwordDelimiter  = "\x1F" // ASCII Unit Separator
)

var (
    emailPatterns = map[string]*regexp.Regexp{
        "gmail.com":      regexp.MustCompile(`^[a-zA-Z0-9._%+\-]+$`),
        "outlook.com":    regexp.MustCompile(`^[a-zA-Z0-9._\-]+$`),
        "hotmail.com":    regexp.MustCompile(`^[a-zA-Z0-9._\-]+$`),
        "yahoo.com":      regexp.MustCompile(`^[a-zA-Z0-9_.]+$`),
        "protonmail.com": regexp.MustCompile(`^[a-zA-Z0-9._%+\-]+$`),
    }
    // General RFC 5322 pattern for other domains (case-insensitive)
    generalEmailRegex = regexp.MustCompile(`(?i)(?:[a-z0-9!#$%&'*+/=?^_` + "`" + `{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_` + "`" + `{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9\-]+\.)+[a-z0-9\-]+|\[[^\]]+\])`)
    threshold = 0.5 // Hybrid Similarity Score acceptance threshold
    w1 = 0.5 // Weight for freqSimilarity
    w2 = 0.5 // Weight for orderSimilarity
    maxEntriesPerBucket = 1000
    scoreRangeCounter = map[string]int{
        "0":            0,
        "0.0001-0.0500": 0,
        "0.0501-0.1000": 0,
        "0.1001-0.1500": 0,
        "0.1501-0.2000": 0,
        "0.2001-0.2500": 0,
        "0.2501-0.3000": 0,
        "0.3001-0.3500": 0,
        "0.3501-0.4000": 0,
        "0.4001-0.4500": 0,
        "0.4501-0.5000": 0,
        "0.5001-0.5500": 0,
        "0.5501-0.6000": 0,
        "0.6001-0.6500": 0,
        "0.6501-0.7000": 0,
        "0.7001-0.7500": 0,
        "0.7501-0.8000": 0,
        "0.8001-0.8500": 0,
        "0.8501-0.9000": 0,
        "0.9001-0.9500": 0,
        "0.9501-0.9999": 0,
        "1":            0,
    }
    caseInsensitiveScoreRangeCounter = map[string]int{
        "0":            0,
        "0.0001-0.0500": 0,
        "0.0501-0.1000": 0,
        "0.1001-0.1500": 0,
        "0.1501-0.2000": 0,
        "0.2001-0.2500": 0,
        "0.2501-0.3000": 0,
        "0.3001-0.3500": 0,
        "0.3501-0.4000": 0,
        "0.4001-0.4500": 0,
        "0.4501-0.5000": 0,
        "0.5001-0.5500": 0,
        "0.5501-0.6000": 0,
        "0.6001-0.6500": 0,
        "0.6501-0.7000": 0,
        "0.7001-0.7500": 0,
        "0.7501-0.8000": 0,
        "0.8001-0.8500": 0,
        "0.8501-0.9000": 0,
        "0.9001-0.9500": 0,
        "0.9501-0.9999": 0,
        "1":            0,
    }
    usernamescoreRangeCounter = map[string]int{
        "0":            0,
        "0.0001-0.0500": 0,
        "0.0501-0.1000": 0,
        "0.1001-0.1500": 0,
        "0.1501-0.2000": 0,
        "0.2001-0.2500": 0,
        "0.2501-0.3000": 0,
        "0.3001-0.3500": 0,
        "0.3501-0.4000": 0,
        "0.4001-0.4500": 0,
        "0.4501-0.5000": 0,
        "0.5001-0.5500": 0,
        "0.5501-0.6000": 0,
        "0.6001-0.6500": 0,
        "0.6501-0.7000": 0,
        "0.7001-0.7500": 0,
        "0.7501-0.8000": 0,
        "0.8001-0.8500": 0,
        "0.8501-0.9000": 0,
        "0.9001-0.9500": 0,
        "0.9501-0.9999": 0,
        "1":            0,
    }
    usernamecaseInsensitiveScoreRangeCounter = map[string]int{
        "0":            0,
        "0.0001-0.0500": 0,
        "0.0501-0.1000": 0,
        "0.1001-0.1500": 0,
        "0.1501-0.2000": 0,
        "0.2001-0.2500": 0,
        "0.2501-0.3000": 0,
        "0.3001-0.3500": 0,
        "0.3501-0.4000": 0,
        "0.4001-0.4500": 0,
        "0.4501-0.5000": 0,
        "0.5001-0.5500": 0,
        "0.5501-0.6000": 0,
        "0.6001-0.6500": 0,
        "0.6501-0.7000": 0,
        "0.7001-0.7500": 0,
        "0.7501-0.8000": 0,
        "0.8001-0.8500": 0,
        "0.8501-0.9000": 0,
        "0.9001-0.9500": 0,
        "0.9501-0.9999": 0,
        "1":            0,
    }
    commonUsernames = []string{
        "email", "enquire", "enquiries", "inquiry", "ask", "info", "support", "help", "contact", 
        "hotline", "customer", "customerservice", "client", "user", "feedback", "complaints", 
        "admin", "administrator", "sysadmin", "it", "root", "hostmaster", "postmaster", "webmaster",
        "moderator", "security", "helpdesk", "desk", "abuse", "alerts", "notifications", "bugreport",
        "billing", "accounting", "finance", "payroll", "payments", "revenue", "invoices", "hr",
        "careers", "hiring", "jobs", "recruitment", "talent", "training", "onboarding",
        "ceo", "cfo", "cto", "cio", "coo", "vp", "founder", "owner", "partner",
        "manager", "director", "board", "leader", "leadership", "executive",
        "press", "media", "marketing", "branding", "sales", "promotion", "newsletter",
        "publicrelations", "pr", "affiliates", "campaign", "sponsorships", 
        "developer", "dev", "engineer", "engineering", "developerrelations", "supportteam",
        "devops", "technology", "architecture", "design", "ux", "ui", "designer",
        "orders", "order", "booking", "bookings", "reservations", "reservation",
        "noreply", "no-reply", "bot", "mailer-daemon", "service", "services", "updates",
        "example", "examples", "test", "sandbox", "demo", "trial", "dummy", "qa", "staging",
        "students", "faculty", "staff", "university", "college", "admissions", "registrar",
        "legal", "compliance", "regulations", "privacy", "gdpr", "audit", "law", "terms",
        "weather", "alerts", "emergency", "health", "safety", "disaster", "insurance",
    }

    ianaReservedDomains = map[string]struct{}{
        "example.com": {}, "example.net": {}, "example.org": {},
        "test": {}, "invalid": {}, "localhost": {}, "example": {}, "local": {},
    }
    disposableEmailDomains = map[string]struct{}{
        "mailinator.com": {}, "10minutemail.com": {}, "guerrillamail.com": {}, "tempmail.com": {}, "yopmail.com": {},
        "trashmail.com": {}, "sharklasers.com": {}, "maildrop.cc": {}, "spamgourmet.com": {}, "inbox.lv": {}, "tempinbox.com": {},
        "trashmail.net": {}, "throwawaymail.com": {}, "dispostable.com": {},
    }
)

type UserStats struct {
    EmailDomains []string
    Passwords    []string
    Countries    []string
    DomainCount  int
    PasswordCount int
}

type UserStatsJSON struct {
    ComboCounts       map[string]int `json:"combo_counts"`
    ScoreRangeCounter map[string]int `json:"score_range_counter"`
    CaseInsensitiveScoreRangeCounter    map[string]int `json:"case_insensitive_score_range_counter"`
    UsernameScoreRangeCounter           map[string]int `json:"username_score_range_counter"`
    UsernameCaseInsensitiveScoreRangeCounter map[string]int `json:"username_case_insensitive_score_range_counter"`
}

type SummaryData struct {
    TotalUsernames       int            `json:"total_usernames"`
    TotalUniquePasswords uint64         `json:"total_unique_passwords"`
    TotalPasswordPairs   int            `json:"total_password_pairs"`
    CountryCounts        map[string]int `json:"country_counts"`
    ComboCounts          map[string]int `json:"combo_counts"`
    ScoreRangeCounter    map[string]int `json:"case_sensitive_score_range_counter"`
    CaseInsensitiveScoreRangeCounter    map[string]int `json:"case_insensitive_score_range_counter"`
    HLLState             []byte         `json:"hll_state"`
}

func main() {
    if len(os.Args) != 2 {
        fmt.Println("Usage: go run process_breached_dataset.go <output_directory>")
        os.Exit(1)
    }

    outputDir := filepath.Clean(os.Args[1])
    if err := os.MkdirAll(outputDir, 0755); err != nil {
        fmt.Fprintf(os.Stderr, "Error creating output directory: %v\n", err)
        os.Exit(1)
    }

    extensionMapping, err := loadExtensionMapping("tld_country_code.csv")
    if err != nil {
        fmt.Fprintf(os.Stderr, "Failed to load extension mapping: %v\n", err)
        os.Exit(1)
    }

    scanner := bufio.NewScanner(os.Stdin)
    const maxCapacity = 1000 * 1024 * 1024 // 100MB
    buf := make([]byte, maxCapacity)
    scanner.Buffer(buf, maxCapacity)

    // Step 1: Parse Data and Build Connections
    // A map to store {username: [[email_domain, password, country], [email_domain, password, country]]}
    usernameRecords := make(map[string][][]string)
    uniqueCountryCounts := make(map[string]map[string]struct{})
    countryCounts := make(map[string]int)
    commonUsernameSet := createCommonUsernameSet()
    for scanner.Scan() {
        entry := scanner.Text()
        entry = strings.TrimSpace(entry)
        if !strings.Contains(entry, ":") {
            continue
        }

        parts := strings.SplitN(entry, ":", 2)
        if len(parts) != 2 {
            continue
        }

        email := strings.TrimSpace(parts[0])
        if !isValidEmail(email) {
            continue
        }

        password := strings.TrimSpace(parts[1])
        if !isValidPassword(password) {
            continue
        }

        atIndex := strings.LastIndex(email, "@")
        if atIndex == -1 || atIndex == len(email)-1 {
            continue
        }

        username := email[:atIndex]
        email_domain := strings.ToLower(email[atIndex+1:])
        if isIANAReservedDomain(email_domain) || isDisposableEmail(email_domain) {
            //fmt.Printf("Skipping IANA reserved domain: %s\n", email)
            //fmt.Printf("Skipping disposable email: %s\n", email)
            continue
        }
        country := getCountryForDomain(email_domain, extensionMapping)

        if _, exists := uniqueCountryCounts[country]; !exists {
            uniqueCountryCounts[country] = make(map[string]struct{})
        }
        uniqueCountryCounts[country][email_domain] = struct{}{}
        //fmt.Printf("DEBUG: %s\n", entry)
        if isCommonUsername(username, commonUsernameSet) {
            username = email
        }
        usernameRecords[username] = append(usernameRecords[username], []string{email_domain, password, country})
    }

    // Step 2: Generate reports
    rand.Seed(time.Now().UnixNano())
    userStats, comboCounts := collectUserStats(usernameRecords)
    for country, domains := range uniqueCountryCounts {
        countryCounts[country] = len(domains) // Only count unique domains
    }
    writeCountryAggregationCSV(outputDir, countryCounts)  
    //writeUserPasswordsReportCSV(outputDir, userStats) // data.csv to big to open
    writeSuspiciousUsersReportCSV(outputDir, userStats)
    writeUsersBlocklistReportCSV(outputDir, userStats)
    writePasswordPairsCSV(outputDir, userStats)
    //writeUserStatsCSV(outputDir, comboCounts)
    writeUserStatsJSON(outputDir, comboCounts, scoreRangeCounter, caseInsensitiveScoreRangeCounter)
    summaryFile := filepath.Join(".", "summary.json")
    updateSummary(summaryFile, userStats, comboCounts, countryCounts, scoreRangeCounter, caseInsensitiveScoreRangeCounter)
}

func isValidEmail(email string) bool {
    atIndex := strings.LastIndex(email, "@")
    if atIndex == -1 || atIndex == len(email)-1 {
        return false
    }

    localPart := email[:atIndex]
    domain := strings.ToLower(email[atIndex+1:])

    for baseDomain, pattern := range emailPatterns {
        // Accept if:
        //   1. The domain exactly matches the base domain, or
        //   2. The domain starts with the base domain followed by a dot.
        if domain == baseDomain || (strings.HasPrefix(domain, baseDomain) &&
            len(domain) > len(baseDomain) &&
            domain[len(baseDomain)] == '.') {
            return pattern.MatchString(localPart)
        }
    }

    return generalEmailRegex.MatchString(email)
}

func isValidPassword(password string) bool {
    if strings.TrimSpace(password) == "" {
        return false
    }
    if len(password) < 8 || len(password) > 64 {
        return false
    }
    // Use RuneCountInString to correctly count characters
    runeCount := utf8.RuneCountInString(password)
    if runeCount < 8 || runeCount > 64 {
        return false
    }
    if !utf8.ValidString(password) {
        return false
    }
    for _, r := range password {
        if !unicode.IsPrint(r) {
            return false
        }
    }
    return true
}

func getCountryForDomain(domain string, mapping map[string]string) string {
    idx := strings.LastIndex(domain, ".")
    if idx == -1 {
        return "Global"
    }
    ext := domain[idx:]
    if country, ok := mapping[ext]; ok {
        return country
    }
    return "Global"
}

func createCommonUsernameSet() map[string]struct{} {
    commonSet := make(map[string]struct{}, len(commonUsernames))
    for _, username := range commonUsernames {
        commonSet[username] = struct{}{}
    }
    return commonSet
}

func isCommonUsername(username string, commonSet map[string]struct{}) bool {
    username = strings.ToLower(username)
    _, exists := commonSet[username]
    return exists
}

func isIANAReservedDomain(domain string) bool {
    domain = strings.ToLower(domain) // Normalize case
    _, exists := ianaReservedDomains[domain]
    return exists
}

func isDisposableEmail(domain string) bool {
    domain = strings.ToLower(domain)
    _, exists := disposableEmailDomains[domain]
    return exists
}

func collectUserStats(usernameRecords map[string][][]string) (map[string]UserStats, map[string]int) {
    userStats := make(map[string]UserStats)
    comboCounts := make(map[string]int)

    for username, records := range usernameRecords {
        emailDomainsSet := make(map[string]struct{}) 
        passwordsSet := make(map[string]struct{})    
        countriesSet := make(map[string]struct{})    

        for _, record := range records {
            emailDomain := record[0]
            password := record[1]
            country := record[2]

            emailDomainsSet[emailDomain] = struct{}{}
            passwordsSet[password] = struct{}{}
            if country != "" {
                countriesSet[country] = struct{}{}
            }
            updateUsernamescoreRangeCounter(hybridSimilarity(username, password, w1, w2))
            updateUsernamecaseInsensitiveScoreRangeCounter(hybridSimilarity(strings.ToLower(username), strings.ToLower(password), w1, w2))
        }

        emailDomains := sortKeys(emailDomainsSet)
        passwords := sortKeys(passwordsSet)
        countries := sortKeys(countriesSet)

        userStats[username] = UserStats{
            EmailDomains: emailDomains,
            Passwords:    passwords,
            Countries:    countries,
            DomainCount:  len(emailDomains),
            PasswordCount: len(passwords),
        }
        // format: "domain_count:password_count"
        comboKey := fmt.Sprintf("%d:%d", len(emailDomains), len(passwords))
        comboCounts[comboKey]++
    }

    return userStats, comboCounts
}

func sortKeys(data map[string]struct{}) []string {
    keys := make([]string, 0, len(data))
    for key := range data {
        keys = append(keys, key)
    }
    sort.Strings(keys)
    return keys
}

func createCSVWriter(filename, outputDir string, header []string) (*csv.Writer, *os.File, error) {
    filepath := filepath.Join(outputDir, filename)
    file, err := os.Create(filepath)
    if err != nil {
        return nil, nil, fmt.Errorf("error creating file %s: %v", filepath, err)
    }
    writer := csv.NewWriter(file)
    if err := writer.Write(header); err != nil {
        file.Close()
        return nil, nil, fmt.Errorf("error writing header to %s: %v", filepath, err)
    }
    return writer, file, nil
}

func writeCountryAggregationCSV(outputDir string, countryCounts map[string]int) {
    filename := "geo.csv"
    writer, file, _error := createCSVWriter(filename, outputDir, []string{"country", "frequency"})
    if _error != nil {
        log.Fatal(_error)
    }
    defer file.Close()
    defer writer.Flush()

    for country, count := range countryCounts {
        row := []string{country, fmt.Sprintf("%d", count)}
        if err := writer.Write(row); err != nil {
            fmt.Fprintf(os.Stderr, "Error writing row for country %s: %v\n", country, err)
        }
    }
    fmt.Printf("CSV file '%s' has been created successfully in '%s'.\n", filename, outputDir)
}

func writeUserPasswordsReportCSV(outputDir string, userStats map[string]UserStats) {
    filename := "data.csv"
    writer, file, _error := createCSVWriter(filename, outputDir, []string{"username", "password_count", "passwords", "email_domains", "countries"})
    if _error != nil {
        log.Fatal(_error)
    }
    defer file.Close()
    defer writer.Flush()

    for username, stats := range userStats {
        if len(stats.Passwords) >= 1000 {
            continue;
        }
        row := []string{
            username,
            fmt.Sprintf("%d", len(stats.Passwords)),
            strings.Join(stats.Passwords, passwordDelimiter),
            strings.Join(stats.EmailDomains, commonDelimiter),
            strings.Join(stats.Countries, commonDelimiter),
        }
        if err := writer.Write(row); err != nil {
            fmt.Fprintf(os.Stderr, "Error writing row for user_report %s: %v\n", row, err)
        }
    }

    fmt.Printf("CSV file '%s' has been created successfully in '%s'.\n", filename, outputDir)
}

func writeUsersBlocklistReportCSV(outputDir string, userStats map[string]UserStats) {
    filename := "userblocklist.csv"
    writer, file, _error := createCSVWriter(filename, outputDir, []string{""})
    if _error != nil {
        log.Fatal(_error)
    }
    defer file.Close()
    defer writer.Flush()

    for username, stats := range userStats {
        if len(stats.Passwords) < 1000 {
            continue;
        }
        row := []string{username}
        if err := writer.Write(row); err != nil {
            fmt.Fprintf(os.Stderr, "Error writing row for userblocklist %s: %v\n", row, err)
        }
    }

    fmt.Printf("CSV file '%s' has been created successfully in '%s'.\n", filename, outputDir)
}

func writeSuspiciousUsersReportCSV(outputDir string, userStats map[string]UserStats) {
    filename := "userblocklist-stat.csv"
    writer, file, _error := createCSVWriter(filename, outputDir, []string{"username", "password_count", "email_domain_count", "countries"})
    if _error != nil {
        log.Fatal(_error)
    }
    defer file.Close()
    defer writer.Flush()

    for username, stats := range userStats {
        if len(stats.Passwords) < 1000 {
            continue;
        }
        row := []string{
            username,
            fmt.Sprintf("%d", len(stats.Passwords)),
            fmt.Sprintf("%d", len(stats.EmailDomains)),
            strings.Join(stats.Countries, commonDelimiter),
        }
        if err := writer.Write(row); err != nil {
            fmt.Fprintf(os.Stderr, "Error writing row for user_report %s: %v\n", row, err)
        }
    }

    fmt.Printf("CSV file '%s' has been created successfully in '%s'.\n", filename, outputDir)
}


//func writeUserStatsCSV(outputDir string, comboCounts map[string]int) {
//    filename := "stats.csv"
//    writer, file, _error := createCSVWriter(filename, outputDir, []string{"domain-password-combo", "username-count", "similarity-score-range", "count"})
//    if _error != nil {
//        log.Fatal(_error)
//    }
//    defer file.Close()
//    defer writer.Flush()

//    for comboKey, count := range comboCounts {
//        row := []string{comboKey, fmt.Sprintf("%d", count)}
//        if err := writer.Write(row); err != nil {
//            fmt.Fprintf(os.Stderr, "Error writing row for user_stats %s: %v\n", row, err)
//        }
//    }

//    for rangeKey, count := range scoreRangeCounter {
//        row := []string{"", "", rangeKey, fmt.Sprintf("%d", count)}
//        if err := writer.Write(row); err != nil {
//            fmt.Fprintf(os.Stderr, "Error writing row for score_range %s: %v\n", row, err)
//        }
//    }
//    fmt.Printf("CSV file '%s' has been created successfully in '%s'.\n", filename, outputDir)
//}

func writeUserStatsJSON(outputDir string, comboCounts map[string]int, scoreRangeCounter, caseInsensitiveScoreRangeCounter map[string]int) {
    filename := "stats.json"
    filepath := filepath.Join(outputDir, filename)

    // Create JSON structure
    statsData := UserStatsJSON{
        ComboCounts:       comboCounts,
        ScoreRangeCounter: scoreRangeCounter,
        CaseInsensitiveScoreRangeCounter: caseInsensitiveScoreRangeCounter,
        UsernameScoreRangeCounter: usernamescoreRangeCounter,
        UsernameCaseInsensitiveScoreRangeCounter: usernamecaseInsensitiveScoreRangeCounter,
    }

    jsonData, err := json.MarshalIndent(statsData, "", "  ")
    if err != nil {
        log.Fatalf("Error encoding user stats JSON: %v", err)
    }

    err = os.WriteFile(filepath, jsonData, 0644)
    if err != nil {
        log.Fatalf("Error writing JSON file %s: %v", filepath, err)
    }

    fmt.Printf("JSON file '%s' has been created successfully in '%s'.\n", filename, outputDir)
}

func allBucketsFull(bucketCounter map[string]int, maxEntries int) bool {
    for _, count := range bucketCounter {
        if count < maxEntries {
            return false
        }
    }
    return true
}

func writePasswordPairsCSV(outputDir string, userStats map[string]UserStats) {
    fileCounter := 1
    filename := fmt.Sprintf("password_pairs_%d.csv", fileCounter)
    writer, file, _error := createCSVWriter(
        filename,
        outputDir,
        []string{
            "username",
            "hybrid_similarity_score",
            "case_insensitive_similarity_score",
            "username_pw1_similarity",
            "username_pw2_similarity",
            "pw1",
            "pw2",
        },
    )
    if _error != nil {
        log.Fatal(_error)
    }
    defer file.Close()
    bucketCounter := map[string]int{}
    for bucket := range scoreRangeCounter {
        bucketCounter[bucket] = 0
    }

    for username, stats := range userStats {
        passwords := stats.Passwords
        if len(passwords) < 2 || len(passwords) >= 1000 {
            continue;
        }
        // Generate combination of password pairs e.g. (A,B), skipping (B, \A)
        for i := 0; i < len(passwords); i++ {
            for j := i + 1; j < len(passwords); j++ {

                similarityScore := hybridSimilarity(passwords[i], passwords[j], w1, w2)
                caseInsensitiveSimilarityScore := hybridSimilarity(strings.ToLower(passwords[i]), strings.ToLower(passwords[j]), w1, w2)
                updateCaseSensitiveScoreRangeCounter(similarityScore)
                updateCaseInsensitiveScoreRangeCounter(caseInsensitiveSimilarityScore)
                usernamePW1Similarity := hybridSimilarity(username, passwords[i], w1, w2)
                usernamePW2Similarity := hybridSimilarity(username, passwords[j], w1, w2)

                bucketKey := getSimilarityBucket(caseInsensitiveSimilarityScore)
                if bucketCounter[bucketKey] < maxEntriesPerBucket {
                    //passwordPair := passwords[i] + passwordDelimiter + passwords[j]
                    row := []string{
                        username,
                        fmt.Sprintf("%.4f", similarityScore),
                        fmt.Sprintf("%.4f", caseInsensitiveSimilarityScore),
                        fmt.Sprintf("%.4f", usernamePW1Similarity),
                        fmt.Sprintf("%.4f", usernamePW2Similarity),
                        passwords[i],
                        passwords[j],
                    }
                    if err := writer.Write(row); err != nil {
                        fmt.Fprintf(os.Stderr, "Error writing row for password_pairs %s: %v\n", row, err)
                    }
                    bucketCounter[bucketKey]++
                }
                //fmt.Printf("** %v\n", bucketCounter)

                if allBucketsFull(bucketCounter, maxEntriesPerBucket) {
                    writer.Flush()
                    file.Close()
                    fmt.Printf("CSV file '%s' has been created successfully in '%s'.\n", filename, outputDir)

                    for bucket := range bucketCounter {
                        bucketCounter[bucket] = 0
                    }
                    fileCounter++
                    filename = fmt.Sprintf("password_pairs_%d.csv", fileCounter)
                    writer, file, _error = createCSVWriter(
                        filename,
                        outputDir,
                        []string{
                            "username",
                            "hybrid_similarity_score",
                            "case_insensitive_similarity_score",
                            "username_pw1_similarity",
                            "username_pw2_similarity",
                            "pw1",
                            "pw2",
                        },
                    )
                    if _error != nil {
                        log.Fatal(_error)
                    }
                }
                
            }
        }

    }
    writer.Flush()
    file.Close()
    fmt.Printf("--- CSV file '%s' has been created successfully in '%s'.\n", filename, outputDir)
}

func getSimilarityBucket(score float64) string {
    switch {
    case score == 0:
        return "0"
    case score > 0 && score <= 0.05:
        return "0.0001-0.0500"
    case score > 0.05 && score <= 0.1:
        return "0.0501-0.1000"
    case score > 0.1 && score <= 0.15:
        return "0.1001-0.1500"
    case score > 0.15 && score <= 0.2:
        return "0.1501-0.2000"
    case score > 0.2 && score <= 0.25:
        return "0.2001-0.2500"
    case score > 0.25 && score <= 0.3:
        return "0.2501-0.3000"
    case score > 0.3 && score <= 0.35:
        return "0.3001-0.3500"
    case score > 0.35 && score <= 0.4:
        return "0.3501-0.4000"
    case score > 0.4 && score <= 0.45:
        return "0.4001-0.4500"
    case score > 0.45 && score <= 0.5:
        return "0.4501-0.5000"
    case score > 0.5 && score <= 0.55:
        return "0.5001-0.5500"
    case score > 0.55 && score <= 0.6:
        return "0.5501-0.6000"
    case score > 0.6 && score <= 0.65:
        return "0.6001-0.6500"
    case score > 0.65 && score <= 0.7:
        return "0.6501-0.7000"
    case score > 0.7 && score <= 0.75:
        return "0.7001-0.7500"
    case score > 0.75 && score <= 0.8:
        return "0.7501-0.8000"
    case score > 0.8 && score <= 0.85:
        return "0.8001-0.8500"
    case score > 0.85 && score <= 0.9:
        return "0.8501-0.9000"
    case score > 0.9 && score <= 0.95:
        return "0.9001-0.9500"
    case score > 0.95 && score < 1:
        return "0.9501-0.9999"
    case score == 1:
        return "1"
    default:
        return "unknown"
    }
}

func updateCaseSensitiveScoreRangeCounter(similarityScore float64) {
    switch {
        case similarityScore == 0:
            scoreRangeCounter["0"]++
        case similarityScore > 0 && similarityScore <= 0.05:
            scoreRangeCounter["0.0001-0.0500"]++
        case similarityScore > 0.05 && similarityScore <= 0.1:
            scoreRangeCounter["0.0501-0.1000"]++
        case similarityScore > 0.1 && similarityScore <= 0.15:
            scoreRangeCounter["0.1001-0.1500"]++
        case similarityScore > 0.15 && similarityScore <= 0.20:
            scoreRangeCounter["0.1501-0.2000"]++
        case similarityScore > 0.20 && similarityScore <= 0.25:
            scoreRangeCounter["0.2001-0.2500"]++
        case similarityScore > 0.25 && similarityScore <= 0.30:
            scoreRangeCounter["0.2501-0.3000"]++
        case similarityScore > 0.30 && similarityScore <= 0.35:
            scoreRangeCounter["0.3001-0.3500"]++
        case similarityScore > 0.35 && similarityScore <= 0.40:
            scoreRangeCounter["0.3501-0.4000"]++
        case similarityScore > 0.40 && similarityScore <= 0.45:
            scoreRangeCounter["0.4001-0.4500"]++
        case similarityScore > 0.45 && similarityScore <= 0.50:
            scoreRangeCounter["0.4501-0.5000"]++
        case similarityScore > 0.50 && similarityScore <= 0.55:
            scoreRangeCounter["0.5001-0.5500"]++
        case similarityScore > 0.55 && similarityScore <= 0.60:
            scoreRangeCounter["0.5501-0.6000"]++
        case similarityScore > 0.60 && similarityScore <= 0.65:
            scoreRangeCounter["0.6001-0.6500"]++
        case similarityScore > 0.65 && similarityScore <= 0.70:
            scoreRangeCounter["0.6501-0.7000"]++
        case similarityScore > 0.70 && similarityScore <= 0.75:
            scoreRangeCounter["0.7001-0.7500"]++
        case similarityScore > 0.75 && similarityScore <= 0.80:
            scoreRangeCounter["0.7501-0.8000"]++
        case similarityScore > 0.80 && similarityScore <= 0.85:
            scoreRangeCounter["0.8001-0.8500"]++
        case similarityScore > 0.85 && similarityScore <= 0.90:
            scoreRangeCounter["0.8501-0.9000"]++
        case similarityScore > 0.9 && similarityScore <= 0.95:
            scoreRangeCounter["0.9001-0.9500"]++
        case similarityScore > 0.95 && similarityScore < 1:
            scoreRangeCounter["0.9501-0.9999"]++
        case similarityScore == 1:
            scoreRangeCounter["1"]++
    }
}

func updateCaseInsensitiveScoreRangeCounter(similarityScore float64) {
    switch {
        case similarityScore == 0:
            caseInsensitiveScoreRangeCounter["0"]++
        case similarityScore > 0 && similarityScore <= 0.05:
            caseInsensitiveScoreRangeCounter["0.0001-0.0500"]++
        case similarityScore > 0.05 && similarityScore <= 0.1:
            caseInsensitiveScoreRangeCounter["0.0501-0.1000"]++
        case similarityScore > 0.1 && similarityScore <= 0.15:
            caseInsensitiveScoreRangeCounter["0.1001-0.1500"]++
        case similarityScore > 0.15 && similarityScore <= 0.20:
            caseInsensitiveScoreRangeCounter["0.1501-0.2000"]++
        case similarityScore > 0.20 && similarityScore <= 0.25:
            caseInsensitiveScoreRangeCounter["0.2001-0.2500"]++
        case similarityScore > 0.25 && similarityScore <= 0.30:
            caseInsensitiveScoreRangeCounter["0.2501-0.3000"]++
        case similarityScore > 0.30 && similarityScore <= 0.35:
            caseInsensitiveScoreRangeCounter["0.3001-0.3500"]++
        case similarityScore > 0.35 && similarityScore <= 0.40:
            caseInsensitiveScoreRangeCounter["0.3501-0.4000"]++
        case similarityScore > 0.40 && similarityScore <= 0.45:
            caseInsensitiveScoreRangeCounter["0.4001-0.4500"]++
        case similarityScore > 0.45 && similarityScore <= 0.50:
            caseInsensitiveScoreRangeCounter["0.4501-0.5000"]++
        case similarityScore > 0.50 && similarityScore <= 0.55:
            caseInsensitiveScoreRangeCounter["0.5001-0.5500"]++
        case similarityScore > 0.55 && similarityScore <= 0.60:
            caseInsensitiveScoreRangeCounter["0.5501-0.6000"]++
        case similarityScore > 0.60 && similarityScore <= 0.65:
            caseInsensitiveScoreRangeCounter["0.6001-0.6500"]++
        case similarityScore > 0.65 && similarityScore <= 0.70:
            caseInsensitiveScoreRangeCounter["0.6501-0.7000"]++
        case similarityScore > 0.70 && similarityScore <= 0.75:
            caseInsensitiveScoreRangeCounter["0.7001-0.7500"]++
        case similarityScore > 0.75 && similarityScore <= 0.80:
            caseInsensitiveScoreRangeCounter["0.7501-0.8000"]++
        case similarityScore > 0.80 && similarityScore <= 0.85:
            caseInsensitiveScoreRangeCounter["0.8001-0.8500"]++
        case similarityScore > 0.85 && similarityScore <= 0.90:
            caseInsensitiveScoreRangeCounter["0.8501-0.9000"]++
        case similarityScore > 0.9 && similarityScore <= 0.95:
            caseInsensitiveScoreRangeCounter["0.9001-0.9500"]++
        case similarityScore > 0.95 && similarityScore < 1:
            caseInsensitiveScoreRangeCounter["0.9501-0.9999"]++
        case similarityScore == 1:
            caseInsensitiveScoreRangeCounter["1"]++
    }
}

func updateUsernamescoreRangeCounter(similarityScore float64) {
    switch {
        case similarityScore == 0:
            usernamescoreRangeCounter["0"]++
        case similarityScore > 0 && similarityScore <= 0.05:
            usernamescoreRangeCounter["0.0001-0.0500"]++
        case similarityScore > 0.05 && similarityScore <= 0.1:
            usernamescoreRangeCounter["0.0501-0.1000"]++
        case similarityScore > 0.1 && similarityScore <= 0.15:
            usernamescoreRangeCounter["0.1001-0.1500"]++
        case similarityScore > 0.15 && similarityScore <= 0.20:
            usernamescoreRangeCounter["0.1501-0.2000"]++
        case similarityScore > 0.20 && similarityScore <= 0.25:
            usernamescoreRangeCounter["0.2001-0.2500"]++
        case similarityScore > 0.25 && similarityScore <= 0.30:
            usernamescoreRangeCounter["0.2501-0.3000"]++
        case similarityScore > 0.30 && similarityScore <= 0.35:
            usernamescoreRangeCounter["0.3001-0.3500"]++
        case similarityScore > 0.35 && similarityScore <= 0.40:
            usernamescoreRangeCounter["0.3501-0.4000"]++
        case similarityScore > 0.40 && similarityScore <= 0.45:
            usernamescoreRangeCounter["0.4001-0.4500"]++
        case similarityScore > 0.45 && similarityScore <= 0.50:
            usernamescoreRangeCounter["0.4501-0.5000"]++
        case similarityScore > 0.50 && similarityScore <= 0.55:
            usernamescoreRangeCounter["0.5001-0.5500"]++
        case similarityScore > 0.55 && similarityScore <= 0.60:
            usernamescoreRangeCounter["0.5501-0.6000"]++
        case similarityScore > 0.60 && similarityScore <= 0.65:
            usernamescoreRangeCounter["0.6001-0.6500"]++
        case similarityScore > 0.65 && similarityScore <= 0.70:
            usernamescoreRangeCounter["0.6501-0.7000"]++
        case similarityScore > 0.70 && similarityScore <= 0.75:
            usernamescoreRangeCounter["0.7001-0.7500"]++
        case similarityScore > 0.75 && similarityScore <= 0.80:
            usernamescoreRangeCounter["0.7501-0.8000"]++
        case similarityScore > 0.80 && similarityScore <= 0.85:
            usernamescoreRangeCounter["0.8001-0.8500"]++
        case similarityScore > 0.85 && similarityScore <= 0.90:
            usernamescoreRangeCounter["0.8501-0.9000"]++
        case similarityScore > 0.9 && similarityScore <= 0.95:
            usernamescoreRangeCounter["0.9001-0.9500"]++
        case similarityScore > 0.95 && similarityScore < 1:
            usernamescoreRangeCounter["0.9501-0.9999"]++
        case similarityScore == 1:
            usernamescoreRangeCounter["1"]++
    }
}

func updateUsernamecaseInsensitiveScoreRangeCounter(similarityScore float64) {
    switch {
        case similarityScore == 0:
            usernamecaseInsensitiveScoreRangeCounter["0"]++
        case similarityScore > 0 && similarityScore <= 0.05:
            usernamecaseInsensitiveScoreRangeCounter["0.0001-0.0500"]++
        case similarityScore > 0.05 && similarityScore <= 0.1:
            usernamecaseInsensitiveScoreRangeCounter["0.0501-0.1000"]++
        case similarityScore > 0.1 && similarityScore <= 0.15:
            usernamecaseInsensitiveScoreRangeCounter["0.1001-0.1500"]++
        case similarityScore > 0.15 && similarityScore <= 0.20:
            usernamecaseInsensitiveScoreRangeCounter["0.1501-0.2000"]++
        case similarityScore > 0.20 && similarityScore <= 0.25:
            usernamecaseInsensitiveScoreRangeCounter["0.2001-0.2500"]++
        case similarityScore > 0.25 && similarityScore <= 0.30:
            usernamecaseInsensitiveScoreRangeCounter["0.2501-0.3000"]++
        case similarityScore > 0.30 && similarityScore <= 0.35:
            usernamecaseInsensitiveScoreRangeCounter["0.3001-0.3500"]++
        case similarityScore > 0.35 && similarityScore <= 0.40:
            usernamecaseInsensitiveScoreRangeCounter["0.3501-0.4000"]++
        case similarityScore > 0.40 && similarityScore <= 0.45:
            usernamecaseInsensitiveScoreRangeCounter["0.4001-0.4500"]++
        case similarityScore > 0.45 && similarityScore <= 0.50:
            usernamecaseInsensitiveScoreRangeCounter["0.4501-0.5000"]++
        case similarityScore > 0.50 && similarityScore <= 0.55:
            usernamecaseInsensitiveScoreRangeCounter["0.5001-0.5500"]++
        case similarityScore > 0.55 && similarityScore <= 0.60:
            usernamecaseInsensitiveScoreRangeCounter["0.5501-0.6000"]++
        case similarityScore > 0.60 && similarityScore <= 0.65:
            usernamecaseInsensitiveScoreRangeCounter["0.6001-0.6500"]++
        case similarityScore > 0.65 && similarityScore <= 0.70:
            usernamecaseInsensitiveScoreRangeCounter["0.6501-0.7000"]++
        case similarityScore > 0.70 && similarityScore <= 0.75:
            usernamecaseInsensitiveScoreRangeCounter["0.7001-0.7500"]++
        case similarityScore > 0.75 && similarityScore <= 0.80:
            usernamecaseInsensitiveScoreRangeCounter["0.7501-0.8000"]++
        case similarityScore > 0.80 && similarityScore <= 0.85:
            usernamecaseInsensitiveScoreRangeCounter["0.8001-0.8500"]++
        case similarityScore > 0.85 && similarityScore <= 0.90:
            usernamecaseInsensitiveScoreRangeCounter["0.8501-0.9000"]++
        case similarityScore > 0.9 && similarityScore <= 0.95:
            usernamecaseInsensitiveScoreRangeCounter["0.9001-0.9500"]++
        case similarityScore > 0.95 && similarityScore < 1:
            usernamecaseInsensitiveScoreRangeCounter["0.9501-0.9999"]++
        case similarityScore == 1:
            usernamecaseInsensitiveScoreRangeCounter["1"]++
    }
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

func loadExtensionMapping(mappingFile string) (map[string]string, error) {
    cwd, _ := os.Getwd()
    file, err := os.Open(mappingFile)
    mappingFile = filepath.Join(cwd, mappingFile)
    if err != nil {
        return nil, fmt.Errorf("error opening mapping file %s: %v", mappingFile, err)
    }
    defer file.Close()

    reader := csv.NewReader(file)
    records, err := reader.ReadAll()
    if err != nil {
        return nil, fmt.Errorf("error reading mapping CSV file %s: %v", mappingFile, err)
    }

    mapping := make(map[string]string)
    for i, record := range records {
        if i == 0 {
            continue // skip header
        }
        if len(record) < 2 {
            continue // skip invalid rows
        }
        ext := strings.TrimSpace(record[0])
        country := strings.TrimSpace(record[1])
        if !strings.HasPrefix(ext, ".") {
            ext = "." + ext
        }
        mapping[ext] = country
    }
    return mapping, nil
}

func loadSummary(summaryFile string) (SummaryData, error) {
    data := SummaryData{
        CountryCounts: make(map[string]int),
        ComboCounts:   make(map[string]int),
    }

    file, err := ioutil.ReadFile(summaryFile)
    if err != nil {
        return data, nil
    }

    if err := json.Unmarshal(file, &data); err != nil {
        return data, err
    }
    return data, nil
}

func updateSummary(summaryFile string, userStats map[string]UserStats, comboCounts map[string]int, countryCounts map[string]int, scoreRangeCounter, caseInsensitiveScoreRangeCounter map[string]int) {
    summary, err := loadSummary(summaryFile)
    if err != nil {
        fmt.Fprintf(os.Stderr, "Error loading summary: %v\n", err)
        return
    }

    hll := hyperloglog.New()

    if len(summary.HLLState) > 0 {
        prevHLL := hyperloglog.New()
        if err := prevHLL.UnmarshalBinary(summary.HLLState); err != nil {
            fmt.Fprintf(os.Stderr, "Error restoring HLL state: %v\n", err)
        } else {
            hll.Merge(prevHLL) // Merge with previous dataset
        }
    }

    for _, stats := range userStats {
        for _, password := range stats.Passwords {
            hll.Insert([]byte(password))
        }
    }

    summary.TotalUsernames += len(userStats)
    totalPasswordPairs := 0
    for _, count := range scoreRangeCounter {
        totalPasswordPairs += count
    }
    summary.TotalPasswordPairs += totalPasswordPairs
    summary.TotalUniquePasswords = uint64(hll.Estimate())

    encodedHLL, err := hll.MarshalBinary()
    if err != nil {
        fmt.Fprintf(os.Stderr, "Error encoding HLL: %v\n", err)
        return
    }
    summary.HLLState = encodedHLL

    for country, count := range countryCounts {
        summary.CountryCounts[country] += count
    }

    for combo, count := range comboCounts {
        summary.ComboCounts[combo] += count
    }

    if summary.ScoreRangeCounter == nil {
        summary.ScoreRangeCounter = make(map[string]int)
    }
    for rangeKey, count := range scoreRangeCounter {
        summary.ScoreRangeCounter[rangeKey] += count
    }

    if summary.CaseInsensitiveScoreRangeCounter == nil {
        summary.CaseInsensitiveScoreRangeCounter = make(map[string]int)
    }
    for rangeKey, count := range caseInsensitiveScoreRangeCounter {
        summary.CaseInsensitiveScoreRangeCounter[rangeKey] += count
    }

    summaryBytes, err := json.MarshalIndent(summary, "", "  ")
    if err != nil {
        fmt.Fprintf(os.Stderr, "Error marshaling summary: %v\n", err)
        return
    }

    if err := ioutil.WriteFile(summaryFile, summaryBytes, 0644); err != nil {
        fmt.Fprintf(os.Stderr, "Error writing summary file: %v\n", err)
    }
    fmt.Printf("summary.json updated")
}
