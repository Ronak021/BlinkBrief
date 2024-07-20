/*
    This script is responsible for the functionality of the Youtube Transcript Summarizer Chrome extension's popup.
    When the "Summarize" button is clicked, it sends a request to the Flask server to fetch the summarized transcript
    of the currently active YouTube video. 
*/


const summarizeBtn = document.getElementById("summarize");
const downloadBtn = document.getElementById("download");
const downloadContainer = document.getElementById("download-container");



summarizeBtn.addEventListener("click", function() {
    summarizeBtn.disabled = true;
    summarizeBtn.innerHTML = "Summarizing...";
    // downloadBtn.style.display = "none";
    downloadContainer.style.display = "none";
    chrome.tabs.query({ currentWindow: true, active: true }, function(tabs) {
        var url = tabs[0].url;
        var language = document.getElementById("language").value || "en"; // Default language is English
        var summaryLength= document.getElementById("summaryLength").value || "short"; 
        var xhr = new XMLHttpRequest();
        xhr.open("GET", "http://127.0.0.1:5000/summary?url=" + url + "&language=" + language + "&summaryLength=" + summaryLength, true);
        xhr.onload = function() {
            var text = xhr.responseText;
            const output = document.getElementById("output");
            if (xhr.status === 404) {
                output.innerHTML = "Transcript Not Available";
            } else {
                output.innerHTML = text;
                downloadContainer.style.display = "block";
                downloadBtn.style.display = "block"; // Show download button
                downloadBtn.addEventListener("click", function() {
                    // Trigger download action
                    const format = document.getElementById("downloadFormat").value;
                    downloadSummary(text, format);
                });
            }
            summarizeBtn.disabled = false;
            summarizeBtn.innerHTML = "Summarize";
        }
        xhr.send();
    });
});



function downloadSummary(summaryText, format) {
    if (format === 'text') {
      // Create a new Blob object
      var blob = new Blob([summaryText], { type: "text/plain;charset=utf-8" });
      // Create a temporary anchor element
      var a = document.createElement("a");
      a.href = URL.createObjectURL(blob);
      // Set the file name
      a.download = "summary.txt";
      // Append the anchor to the body
      document.body.appendChild(a);
      // Click the anchor to trigger download
      a.click();
      // Remove the anchor from the body
      document.body.removeChild(a);
    } else if (format === 'pdf') {
      const { jsPDF } = window.jspdf; // Make sure jsPDF is loaded
      if (!jsPDF) {
        console.error("jsPDF library is not loaded");
        return;
      }
    
      // Create a new jsPDF instance
      const doc = new jsPDF();
    
      // Set the font and font size (use a font that supports Hindi and Gujarati)
      doc.addFont('fonts/NotoSans-Regular.ttf', 'NotoSans', 'normal'); // Add NotoSans font
      doc.setFont('NotoSans', 'normal');
      doc.setFontSize(12);
    
      // Calculate the number of lines in the summary text
      const lines = doc.splitTextToSize(summaryText, 180);
    
      // Calculate the number of pages needed
      const lineHeight = 10; // adjust this value to fit your needs
      const pageSize = 25; // adjust this value to fit your needs (approx. 25 lines per page)
      let numPages = 1;
      let currentPage = 0;
      let currentLine = 0;
    
      // Add the lines to the PDF document with utf-8 encoding
      for (let i = 0; i < lines.length; i++) {
        if (currentLine >= pageSize) {
          numPages++;
          currentPage++;
          currentLine = 0;
          doc.addPage();
        }
    
        doc.text(lines[i], 10, 10 + (currentLine * lineHeight));
        currentLine++;
      }
    
      // Create a blob from the PDF document
      const pdfBlob = doc.output('blob');
    
      // Use the chrome.downloads API to download the PDF file
      chrome.downloads.download({
        url: URL.createObjectURL(pdfBlob),
        filename: 'Summary.pdf',
        saveAs: true
      });
    }
  }