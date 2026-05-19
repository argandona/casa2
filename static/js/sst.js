document.getElementById('excel_upload').addEventListener('change', function() {
    if (this.files.length > 0) {
        document.getElementById('loading').style.display = 'flex';
    }
});
