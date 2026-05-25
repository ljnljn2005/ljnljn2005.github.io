# ljnljn 的博客

这是一个由 Hexo 驱动、Redefine 主题呈现，并通过 GitHub Actions 发布到 GitHub Pages 的个人博客。

## 常用命令

```powershell
npm install
npm run server
npm run build
```

本仓库已配置本地 Git 提交钩子，用来在提交前拦截常见 API key。首次克隆后可运行：

```powershell
git config core.hooksPath .githooks
```

新建文章：

```powershell
npx hexo new "文章标题"
```

推送到 `main` 分支后，GitHub Actions 会自动构建并发布到：

```text
https://ljnljn2005.github.io
```
