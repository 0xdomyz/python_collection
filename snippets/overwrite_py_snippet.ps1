param(
	[Parameter(Mandatory = $true, Position = 0)]
	[string]$UserName
)

Copy-Item -Force .\snippets_combined.json "C:\Users\$UserName\AppData\Roaming\Code\User\snippets\python.json"