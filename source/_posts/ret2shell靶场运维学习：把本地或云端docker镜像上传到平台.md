---
title: "ret2shell靶场运维学习：把本地或云端docker镜像上传到平台"
date: 2026-05-19 16:34:00
categories:
  - "Security Notes"
tags:
  - "Security"
  - "Linux"
cnblogs_postid: "20082950"
cnblogs_url: "https://www.cnblogs.com/ljnljn/p/20082950"
---

# Ret2Shell 使用本地/超长 Docker 镜像
前提是要把镜像搜索功能关闭，可以看前一篇帖子：https://www.cnblogs.com/ljnljn/p/20082947

## 目标

让 Ret2Shell 平台启动题目环境时使用你本地构建的镜像，而不是去公网 Docker Hub 拉取。

## 关键概念

平台创建的是 Kubernetes Pod。Kubernetes 节点默认看不到你本机 Docker 里的镜像。

所以不要只在本机保留：

```bash
phpserialize-labs:latest
```

而是要把镜像推送到平台内置 registry，再让平台使用完整镜像地址。

当前平台 registry 地址：

```text
localhost:30310
```

镜像地址示例：

```text
localhost:30310/phpserialize-labs:v1
```

## 推荐做法：不用 latest

每次构建后使用固定版本 tag，不复用 `latest`。

例如：

```bash
docker tag phpserialize-labs:latest localhost:30310/phpserialize-labs:v1
docker push localhost:30310/phpserialize-labs:v1
```

如果后续镜像有更新，换一个新 tag：

```bash
docker tag phpserialize-labs:latest localhost:30310/phpserialize-labs:v2
docker push localhost:30310/phpserialize-labs:v2
```

## 平台里怎么填

容器名称字段只填 Kubernetes 容器名，不能填镜像地址。

正确示例：

```text
容器名称：phpserialize-labs
镜像标签：localhost:30310/phpserialize-labs:v1
```

这里注意公网镜像直接写到镜像标签即可

容器名称规则：

```text
3-40 位
以小写字母开头
只能包含小写字母、数字、连字符 -
不能以连字符结尾
```

所以这些是错误的容器名称：

```text
localhost:30310/phpserialize-labs:v1
phpserialize_labs
PhpSerialize
phpserialize-labs-
```

## 如果使用比赛 bucket（目前用不上）

有些场景会按比赛 bucket 隔离镜像，可以把镜像推到 bucket 路径下：

```bash
docker tag phpserialize-labs:latest localhost:30310/<bucket>/phpserialize-labs:v1
docker push localhost:30310/<bucket>/phpserialize-labs:v1
```

平台里填：

```text
localhost:30310/<bucket>/phpserialize-labs:v1
```

## 常见问题

### 保存失败: undefined

通常是题目处于公开状态，Ret2Shell 不允许公开题目时修改环境配置。

处理：

1. 先把题目 Down / 隐藏 / 下线
2. 修改并保存环境配置
3. 再把题目 Up / 公开

### 平台仍然去公网拉取

通常原因：

- 镜像字段没有填写完整 registry 地址
- 把镜像地址误填到了“容器名称”字段
- 使用了 `phpserialize-labs:v1`，Kubernetes 会解析成 Docker Hub 镜像
- Kubernetes 节点访问不到 `localhost:30310`

应填写：

```text
localhost:30310/phpserialize-labs:v1
```

### docker push 报 HTTPS 或 insecure registry 错误

需要让 Docker daemon 允许不安全 registry：

```json
{
  "insecure-registries": ["localhost:30310"]
}
```

修改后重启 Docker。

### localhost:30310 到底是什么

它是平台内置 registry 暴露出来的地址。

流程是：

```text
本地 Docker 镜像
  -> docker push 到 localhost:30310
  -> Kubernetes 节点从 localhost:30310 拉取
  -> 平台启动题目容器
```

如果 Kubernetes 节点和你执行 `docker push` 的机器不是同一台，`localhost:30310` 可能不适合给节点拉取，需要改成节点可访问的 IP 或域名。
