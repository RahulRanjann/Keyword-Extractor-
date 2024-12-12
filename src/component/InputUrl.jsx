import React, { useState } from "react";
import axios from "axios";

export default function InputUrl() {
  const [url, setUrl] = useState("");
  const [result, setResult] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [keywordsTable, setKeywordsTable] = useState([]);
  const [loadingKeywords, setLoadingKeywords] = useState({});
  const [extractingAll, setExtractingAll] = useState(false);

  // Function to extract keywords for a specific blog post
  const extractKeywords = async (link, title) => {
    setLoadingKeywords((prev) => ({ ...prev, [title]: true }));
    try {
      const response = await axios.post(
        "http://localhost:5000/extract-keywords",
        { url: link }
      );
      const extractedKeywords = response.data.keywords || [];

      setKeywordsTable((prev) => {
        const existingitemIndex = prev.findIndex(
          (item) => item.title === title
        );
        if (existingitemIndex !== -1) {
          const updatedTable = [...prev];
          updatedTable[existingitemIndex].keywords = [
            ...new Set([
              ...updatedTable[existingitemIndex].keywords,
              ...extractedKeywords,
            ]),
          ];
          return updatedTable;
        }
        return [...prev, { title, keywords: extractedKeywords }];
      });
    } catch (err) {
      console.error("Error extracting keywords:", err);
      alert(
        `Failed to extract keywords: ${
          err.response?.data?.error || err.message
        }`
      );
    } finally {
      setLoadingKeywords((prev) => ({ ...prev, [title]: false }));
    }
  };

  // Function to extract keywords for all blog posts
  const extractAllKeywords = async () => {
    setExtractingAll(true);
    const promises = result.map((item) =>
      extractKeywords(item.link, item.title)
    );
    try {
      await Promise.all(promises);
    } catch (err) {
      console.error("Error extracting all keywords:", err);
      alert("Failed to extract keywords for all titles.");
    } finally {
      setExtractingAll(false);
    }
  };

  // Function to handle form submission
  const handleScrape = async () => {
    if (!url) {
      alert("Please enter a URL!");
      return;
    }

    setLoading(true);
    setError("");
    try {
      const response = await axios.post("http://localhost:5000/scrape", {
        url,
      });
      setResult(response.data);
      setKeywordsTable([]); // Clear previous keywords when starting new scrape
    } catch (err) {
      setError(
        "Error scraping the website: " +
          (err.response?.data?.error || err.message)
      );
    } finally {
      setLoading(false);
    }
  };

  // Function to copy keywords to clipboard
  const copyToClipboard = (keywords) => {
    const keywordsText = keywords.join(", ");
    navigator.clipboard.writeText(keywordsText).then(
      () => alert("Keywords copied to clipboard!"),
      (err) => alert("Failed to copy keywords: " + err)
    );
  };

  return (
    <div
      className="App"
      style={{
        fontFamily: "Arial, sans-serif",
        maxWidth: "1200px",
        margin: "0 auto",
        padding: "20px",
      }}
    >
      <h1 style={{ textAlign: "center", color: "#333" }}>Blog Scraper</h1>
      <div style={{ display: "flex", marginBottom: "20px" }}>
        <input
          type="text"
          placeholder="Enter blog URL"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          style={{
            flex: 1,
            padding: "10px",
            fontSize: "16px",
            border: "1px solid #ddd",
            marginRight: "10px",
          }}
        />
        <button
          onClick={handleScrape}
          disabled={loading}
          style={{
            padding: "10px 15px",
            backgroundColor: loading ? "#cccccc" : "#4CAF50",
            color: "white",
            border: "none",
            cursor: loading ? "not-allowed" : "pointer",
          }}
        >
          {loading ? "Scraping..." : "Start Scraping"}
        </button>
      </div>

      {error && <p style={{ color: "red", textAlign: "center" }}>{error}</p>}

      {result.length > 0 && (
        <>
          <button
            onClick={extractAllKeywords}
            disabled={extractingAll}
            style={{
              marginTop: "20px",
              padding: "10px 15px",
              backgroundColor: extractingAll ? "#cccccc" : "#007BFF",
              color: "white",
              border: "none",
              cursor: extractingAll ? "not-allowed" : "pointer",
              display: "block",
              marginLeft: "auto",
              marginRight: "auto",
            }}
          >
            {extractingAll ? "Extracting All..." : "Extract All Keywords"}
          </button>

          <table
            style={{
              width: "100%",
              borderCollapse: "collapse",
              marginTop: "20px",
              border: "2px solid #333",
            }}
          >
            <thead>
              <tr style={{ backgroundColor: "#f2f2f2" }}>
                <th
                  style={{
                    border: "1px solid #333",
                    padding: "8px",
                    textAlign: "center",
                  }}
                >
                  Sr. No.
                </th>
                <th
                  style={{
                    border: "1px solid #333",
                    padding: "8px",
                    textAlign: "center",
                  }}
                >
                  Title
                </th>
                <th
                  style={{
                    border: "1px solid #333",
                    padding: "8px",
                    textAlign: "center",
                  }}
                >
                  Image
                </th>
                <th
                  style={{
                    border: "1px solid #333",
                    padding: "8px",
                    textAlign: "center",
                  }}
                >
                  Updates
                </th>
                <th
                  style={{
                    border: "1px solid #333",
                    padding: "8px",
                    textAlign: "center",
                  }}
                >
                  blog URL
                </th>
                <th
                  style={{
                    border: "1px solid #333",
                    padding: "8px",
                    textAlign: "center",
                  }}
                >
                  Keywords
                </th>
                <th
                  style={{
                    border: "1px solid #333",
                    padding: "8px",
                    textAlign: "center",
                  }}
                >
                  Actions
                </th>
              </tr>
            </thead>
            <tbody>
              {result.map((item, index) => (
                <tr
                  key={index}
                  style={{
                    backgroundColor: index % 2 === 0 ? "#ffffff" : "#f0f0f0",
                    border: "1px solid #333",
                  }}
                >
                  <td
                    style={{
                      padding: "8px",
                      textAlign: "center",
                      border: "1px solid #333",
                    }}
                  >
                    {index + 1}
                  </td>
                  <td
                    style={{
                      padding: "8px",
                      textAlign: "left",
                      border: "1px solid #333",
                    }}
                  >
                    {item.title}
                  </td>
                  <td
                    style={{
                      padding: "8px",
                      textAlign: "left",
                      border: "1px solid #333",
                    }}
                  >
                    <img
                      src={item.image}
                      alt={item.title}
                      style={{ maxWidth: "100px", maxHeight: "100px" }}
                    />
                  </td>
                  <td
                    style={{
                      padding: "8px",
                      textAlign: "left",
                      border: "1px solid #333",
                    }}
                  >
                    {item.image_alt || "No alt text"}
                  </td>
                  <td
                    style={{
                      padding: "8px",
                      textAlign: "left",
                      border: "1px solid #333",
                    }}
                  >
                    <a href={item.link || "No link"} target="_blank">link</a>
                  </td>
                  <td
  style={{
    padding: "8px",
    textAlign: "left",
    border: "1px solid #333",
  }}
>
  <ul>
    {keywordsTable
      .find((entry) => entry.title === item.title)
      ?.keywords.map((keyword, index) => (
        <li key={index}>{keyword}</li>
      )) || <li>No keywords</li>}
  </ul>
</td>

                  <td
                    style={{
                      padding: "8px",
                      textAlign: "center",
                      border: "1px solid #333",
                    }}
                  >
                    <button
                      onClick={() => copyToClipboard(item.keywords)}
                      style={{
                        padding: "5px 10px",
                        backgroundColor: "#4CAF50",
                        color: "white",
                        border: "none",
                        cursor: "pointer",
                      }}
                    >
                      Copy Keywords
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </>
      )}
    </div>
  );
}
