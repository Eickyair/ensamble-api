if (-not (Test-Path .env)) {
    Copy-Item .env.example .env
}

Get-Content .env | ForEach-Object {
    if ($_ -match '^\s*([^#][^=]*?)\s*=\s*(.*)$') {
        $name = $matches[1]
        $value = $matches[2]
        [Environment]::SetEnvironmentVariable($name, $value, 'Process')
    }
}



uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload