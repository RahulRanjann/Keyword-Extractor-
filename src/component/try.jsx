import React, { useState } from 'react';
import axios from 'axios';

export default function InputUrl() {
  const [url, setUrl] = useState('');
  const [result, setResult] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [keywordsTable, setKeywordsTable] = useState([]);
  const [loadingKeywords, setLoadingKeywords] = useState({}); // Track loading state per button

  // Function to extract keywords for a specific blog post
  const extractKeywords = async (link, title) => {
    setLoadingKeywords(prev => ({ ...prev, [title]: true })); // Set loading state for the clicked button
    try {
      const response = await axios.post('http://localhost:5000/extract-keywords', { url: link });
      const extractedKeywords = response.data.keywords || [];

      // Add to the keywords table, ensuring no duplicates for the title
      setKeywordsTable(prev => {
        const existingEntryIndex = prev.findIndex(item => item.title === title);
        if (existingEntryIndex !== -1) {
          const updatedTable = [...prev];
          updatedTable[existingEntryIndex].keywords = [...new Set([...updatedTable[existingEntryIndex].keywords, ...extractedKeywords])];
          return updatedTable;
        }
        return [...prev, { title, keywords: extractedKeywords }];
      });
    } catch (err) {
      console.error('Error extracting keywords:', err);
      alert(`Failed to extract keywords: ${err.response?.data?.error || err.message}`);
    } finally {
      setLoadingKeywords(prev => ({ ...prev, [title]: false })); // Set loading state back to false for the clicked button
    }
  };

  // Function to handle form submission
  const handleScrape = async () => {
    if (!url) {
      alert("Please enter a URL!");
      return;
    }

    setLoading(true);
    setError('');
    try {
      const response = await axios.post('http://localhost:5000/scrape', { url });
      setResult(response.data);
    } catch (err) {
      setError('Error scraping the website: ' + (err.response?.data?.error || err.message));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App" style={{ fontFamily: 'Arial, sans-serif', maxWidth: '1200px', margin: '0 auto', padding: '20px' }}>
      <h1 style={{ textAlign: 'center', color: '#333' }}>Blog Scraper</h1>
      <div style={{ display: 'flex', marginBottom: '20px' }}>
        <input
          type="text"
          placeholder="Enter blog URL"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          style={{
            flex: 1,
            padding: '10px',
            fontSize: '16px',
            border: '1px solid #ddd',
            marginRight: '10px'
          }}
        />
        <button
          onClick={handleScrape}
          disabled={loading}
          style={{
            padding: '10px 15px',
            backgroundColor: loading ? '#cccccc' : '#4CAF50',
            color: 'white',
            border: 'none',
            cursor: loading ? 'not-allowed' : 'pointer'
          }}
        >
          {loading ? 'Scraping...' : 'Start Scraping'}
        </button>
      </div>

      {error && <p style={{ color: 'red', textAlign: 'center' }}>{error}</p>}

      {result.length > 0 && (
        <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '20px', border: '2px solid #333' }}>
          <thead>
            <tr style={{ backgroundColor: '#f2f2f2' }}>
              <th style={{ border: '1px solid #333', padding: '8px', textAlign: 'center' }}>Sr. No.</th>
              <th style={{ border: '1px solid #333', padding: '8px', textAlign: 'center' }}>Title</th>
              <th style={{ border: '1px solid #333', padding: '8px', textAlign: 'center' }}>Image</th>
              <th style={{ border: '1px solid #333', padding: '8px', textAlign: 'center' }}>Uploaded A</th>
              <th style={{ border: '1px solid #333', padding: '8px', textAlign: 'center' }}>Link</th>
              <th style={{ border: '1px solid #333', padding: '8px', textAlign: 'center' }}>Actions</th>
            </tr>
          </thead>
          <tbody>
            {result.map((item, index) => (
              <tr key={index} style={{ backgroundColor: index % 2 === 0 ? '#ffffff' : '#f0f0f0', border: '1px solid #333' }}>
                <td style={{ padding: '8px', textAlign: 'center', border: '1px solid #333' }}>{index + 1}</td>
                <td style={{ padding: '8px', textAlign: 'left', border: '1px solid #333' }}>{item.title}</td>
                <td style={{ padding: '8px', textAlign: 'center', border: '1px solid #333' }}>
                  <img src={item.image} alt={item.title} style={{ maxWidth: '100px', maxHeight: '100px' }} />
                </td>
                <td style={{ padding: '8px', textAlign: 'left', border: '1px solid #333' }}>{item.image_alt || 'No alt text'}</td>
                <td style={{ padding: '8px', textAlign: 'left', border: '1px solid #333' }}>{item.link}</td>
                <td style={{ padding: '8px', textAlign: 'center', border: '1px solid #333' }}>
                  <button
                    onClick={() => extractKeywords(item.link, item.title)}
                    disabled={loadingKeywords[item.title]} // Disable the clicked button while it's loading
                    style={{
                      backgroundColor: '#4CAF50',
                      color: 'white',
                      border: 'none',
                      padding: '5px 10px',
                      cursor: loadingKeywords[item.title] ? 'not-allowed' : 'pointer'
                    }}
                  >
                    {loadingKeywords[item.title] ? 'Extracting...' : 'Extract Keywords'}
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {keywordsTable.length > 0 && (
        <div style={{ marginTop: '40px' }}>
          <h2>Extracted Keywords</h2>
          <table style={{ width: '100%', borderCollapse: 'collapse', border: '2px solid #333' }}>
            <thead>
              <tr style={{ backgroundColor: '#f2f2f2' }}>
                <th style={{ border: '1px solid #333', padding: '8px', textAlign: 'center' }}>Title</th>
                <th style={{ border: '1px solid #333', padding: '8px', textAlign: 'center' }}>Keywords</th>
              </tr>
            </thead>
            <tbody>
              {keywordsTable.map((entry, index) => (
                <tr key={index} style={{ backgroundColor: index % 2 === 0 ? '#ffffff' : '#f0f0f0', border: '1px solid #333' }}>
                  <td style={{ padding: '8px', textAlign: 'left', border: '1px solid #333' }}>{entry.title}</td>
                  <td style={{ padding: '8px', textAlign: 'left', border: '1px solid #333' }}>{'|| ' + entry.keywords.join('; ')}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

