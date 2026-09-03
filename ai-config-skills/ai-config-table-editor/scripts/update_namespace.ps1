<#
OpenAPI 更新单个 Apollo 命名空间（只提交，不发布）

用法示例：
  $env:APOLLO_PORTAL_URL = 'http://<apollo-host>:<port>'
  $env:APOLLO_APP_ID     = 'my-server'
  $env:APOLLO_ENV        = 'DEV'
  $env:APOLLO_CLUSTER    = 'default'
  $env:APOLLO_OPERATOR   = '<portal-user>'
  $env:APOLLO_TOKEN      = '<token>'
  powershell -File update_namespace.ps1 -Namespace ConfShop -JsonPath .\ConfShop.json
#>
param(
    [Parameter(Mandatory = $true)][string]$Namespace,
    [Parameter(Mandatory = $true)][string]$JsonPath,
    [string]$Comment = 'synced from xlsx'
)

$ErrorActionPreference = 'Stop'

$base = "$env:APOLLO_PORTAL_URL/openapi/v1"
$headers = @{ Authorization = $env:APOLLO_TOKEN }
$appId = $env:APOLLO_APP_ID
$envName = $env:APOLLO_ENV
$cluster = $env:APOLLO_CLUSTER
$operator = $env:APOLLO_OPERATOR

if (-not $base -or -not $headers.Authorization -or -not $appId -or -not $envName -or -not $cluster -or -not $operator) {
    throw '缺少环境变量：APOLLO_PORTAL_URL / APOLLO_TOKEN / APOLLO_APP_ID / APOLLO_ENV / APOLLO_CLUSTER / APOLLO_OPERATOR'
}

$desired = [System.IO.File]::ReadAllText($JsonPath, [System.Text.UTF8Encoding]::new($false))
$desiredNorm = $desired.TrimEnd([char[]]"`r`n `t")

$items = Invoke-RestMethod -Uri "$base/envs/$envName/apps/$appId/clusters/$cluster/namespaces/$Namespace/items" -Headers $headers -Method Get
$content = @($items.content | Where-Object { $_.key -eq 'content' } | Select-Object -First 1)
if ($content.Count -ne 1) {
    throw "namespace $Namespace content key not found（可能需先 POST 创建，或该命名空间不存在）"
}

$body = @{
    key                      = 'content'
    value                    = $desired
    comment                  = $Comment
    dataChangeLastModifiedBy = $operator
} | ConvertTo-Json -Compress -Depth 10
$bytes = [System.Text.Encoding]::UTF8.GetBytes($body)

$null = Invoke-RestMethod -Uri "$base/envs/$envName/apps/$appId/clusters/$cluster/namespaces/$Namespace/items/content" `
    -Headers $headers -Method Put -ContentType 'application/json;charset=UTF-8' -Body $bytes

$check = Invoke-RestMethod -Uri "$base/envs/$envName/apps/$appId/clusters/$cluster/namespaces/$Namespace/items" -Headers $headers -Method Get
$saved = @($check.content | Where-Object { $_.key -eq 'content' } | Select-Object -First 1)
if ($saved.Count -ne 1 -or $saved[0].value.TrimEnd([char[]]"`r`n `t") -ne $desiredNorm) {
    throw 'verify failed: stored value differs from generated json'
}

Write-Output "UPLOADED (draft saved, NOT released): $Namespace"
