### Hi there 👋

<img align="left" src="https://github-readme-stats.vercel.app/api?username=hallowelt42&theme=dark">
<img align="right" src="https://github-readme-stats.vercel.app/api/top-langs/?username=hallowelt42&theme=dark">



### :construction_worker: Check out what I'm currently working on
{{range recentContributions 5}}
- [{{.Repo.Name}}]({{.Repo.URL}}){{ with .Repo.Description }} - {{ . }}{{ end }} ({{humanize .OccurredAt}})
{{- end}}

### :seedling: My latest projects
{{range recentRepos 5}}
- [{{.Name}}]({{.URL}}){{ with .Description}} - {{ . }}{{ end }}
{{- end}}

### :telescope: Latest releases I've contributed to
{{range recentReleases 5}}
- [{{.Name}}]({{.URL}}) ([{{.LastRelease.TagName}}]({{.LastRelease.URL}}), {{humanize .LastRelease.PublishedAt}}){{ with .Description}} - {{ . }}{{ end }}
{{- end}}
