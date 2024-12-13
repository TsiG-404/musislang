fetch('/path/to/synchronized/lyrics.json')
    .then(response => response.json())
    .then(data => {
        let lyricsContainer = document.getElementById('lyrics');
        data.forEach(item => {
            let timestamp = item.timestamp;  // timestamp in seconds
            let lyric = item.lyric;
            // Display the lyric at the correct time
            setTimeout(() => {
                lyricsContainer.textContent = lyric;
            }, timestamp * 1000);
        });
    });
