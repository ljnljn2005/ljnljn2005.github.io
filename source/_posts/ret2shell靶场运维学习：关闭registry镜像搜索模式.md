---
title: "ret2shell靶场运维学习：关闭registry镜像搜索模式"
date: 2026-05-19 16:34:00
categories:
  - "Security Notes"
tags:
  - "Security"
cnblogs_postid: "20082947"
cnblogs_url: "https://www.cnblogs.com/ljnljn/p/20082947"
---

# Ret2Shell 关闭 Registry 搜索模式完整流程

## 说明

Ret2Shell 的 registry 有两个概念：

```text
registry 服务本身
registry 搜索模式
```

关闭 registry 搜索模式不会关闭 registry 服务。

关闭后：

- 平台前端不会再自动列出 registry 中的镜像和 tag
- 添加题目环境时需要手动填写完整镜像地址
- 已经推送到 registry 的镜像仍然可以被 Kubernetes 拉取

例如仍然可以手动填写：

```text
localhost:30310/phpserialize-labs:v1
```

## 目标效果

平台运行配置中应为：

```toml
[cluster.registry]
enabled = false
server = "ret2shell-registry:5000"
external = "localhost:30310"
insecure = true
```

这里的 `enabled = false` 只表示关闭平台 registry 搜索/选择模式。

## 1. 修改 Helm Chart 默认值

Chart 路径：

```text
/root/ret2shell-src/deploy/helm/ret2shell
```

编辑：

```text
/root/ret2shell-src/deploy/helm/ret2shell/values.yaml
```

在 `registry:` 下加入：

```yaml
registry:
  mode: internal
  replicaCount: 1
  search:
    enabled: false
```

## 2. 修改 Helm 模板

编辑：

```text
/root/ret2shell-src/deploy/helm/ret2shell/templates/_config.tpl
```

找到：

```toml
[cluster.registry]
enabled = true
```

改为：

```gotemplate
[cluster.registry]
enabled = {{ .Values.registry.search.enabled }}
```

这样以后 Helm 渲染出来的配置会跟随 `registry.search.enabled`。

## 3. 修改 values schema

编辑：

```text
/root/ret2shell-src/deploy/helm/ret2shell/values.schema.json
```

在 `registry.properties` 中加入：

```json
"search": {
  "type": "object",
  "properties": {
    "enabled": {
      "type": "boolean"
    }
  }
}
```

## 4. 可选：更新 Chart README

编辑：

```text
/root/ret2shell-src/deploy/helm/ret2shell/README.md
```

在 registry 相关配置处加入：

```text
registry.search.enabled=true|false controls the platform registry search mode
```

## 5. 如果当前运行环境不是重新 Helm 部署

当前平台容器挂载的运行配置来自主机路径：

```text
/srv/ret2shell/backend/config/config.toml
```

需要直接修改这个运行配置。

编辑：

```text
/srv/ret2shell/backend/config/config.toml
```

找到：

```toml
[cluster.registry]
enabled = true
```

改为：

```toml
[cluster.registry]
enabled = false
```

完整示例：

```toml
[cluster.registry]
enabled = false
server = "ret2shell-registry:5000"
external = "localhost:30310"
insecure = true
```

## 6. 重启平台

重启 Ret2Shell 平台 StatefulSet：

```bash
kubectl -n ret2shell-platform rollout restart statefulset/ret2shell-platform
```

等待滚动重启完成：

```bash
kubectl -n ret2shell-platform rollout status statefulset/ret2shell-platform --timeout=180s
```

## 7. 验证 Pod 状态

查看平台 Pod：

```bash
kubectl -n ret2shell-platform get pods -l app.kubernetes.io/component=platform -o wide
```

期望看到：

```text
ret2shell-platform-0   1/1   Running
```

## 8. 验证容器内配置

查看容器内实际生效配置：

```bash
kubectl -n ret2shell-platform exec ret2shell-platform-0 -- sh -c 'sed -n "26,34p" /etc/ret2shell/config.toml'
```

期望看到：

```toml
[cluster.registry]
enabled = false
server = "ret2shell-registry:5000"
external = "localhost:30310"
insecure = true
```

## 9. 验证平台健康

检查 API：

```bash
kubectl -n ret2shell-platform exec ret2shell-platform-0 -- wget -qO- http://127.0.0.1:8080/api/ping
```

期望返回：

```text
pong
```

## 10. 验证前端效果

进入平台题目环境配置页面。

关闭 registry 搜索模式后：

- 不再显示 registry 镜像搜索/选择列表
- 镜像字段需要手动输入完整镜像地址

例如：

```text
localhost:30310/phpserialize-labs:v1
```

容器名称仍然单独填写：

```text
phpserialize-labs
```

## 11. 回滚方法

如果需要重新开启 registry 搜索模式：

运行配置改回：

```toml
[cluster.registry]
enabled = true
```

或者 Helm values 改为：

```yaml
registry:
  search:
    enabled: true
```

然后重启平台：

```bash
kubectl -n ret2shell-platform rollout restart statefulset/ret2shell-platform
kubectl -n ret2shell-platform rollout status statefulset/ret2shell-platform --timeout=180s
```

## 12. 常见问题

### 关闭搜索模式后还能用内置 registry 吗

可以。

关闭的是平台前端的搜索/选择模式，不是 registry 服务。

仍然可以使用：

```bash
docker push localhost:30310/phpserialize-labs:v1
```

然后在平台手动填写：

```text
localhost:30310/phpserialize-labs:v1
```

### 为什么修改 Helm 文件后没有立即生效

因为当前运行中的平台使用的是已经挂载到 Pod 的配置：

```text
/srv/ret2shell/backend/config/config.toml
```

只改 Helm Chart 源文件不会自动修改正在运行的 Pod 配置。

需要：

- 直接修改运行配置并重启平台
- 或重新执行 Helm upgrade 让配置重新渲染并下发

### 如何确认是否真的关闭

以容器内配置为准：

```bash
kubectl -n ret2shell-platform exec ret2shell-platform-0 -- sh -c 'grep -A4 "\\[cluster.registry\\]" /etc/ret2shell/config.toml'
```

看到：

```text
enabled = false
```

即可。
