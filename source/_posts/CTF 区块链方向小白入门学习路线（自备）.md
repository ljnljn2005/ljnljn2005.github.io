---
title: "CTF 区块链方向小白入门学习路线（自备）"
date: 2026-06-12 08:52
categories:
  - "Learning Notes"
tags:
  - "CTF"
  - "Blockchain"
  - "Solidity"
cnblogs_postid: "20465070"
cnblogs_url: "https://www.cnblogs.com/ljnljn/p/20465070"
---

<p>只是给自己看的，ai生成的</p>
<blockquote>
<p>适合对象：刚开始接触 CTF 区块链题、懂一点编程但不了解智能合约安全的同学。<br/>
学习目标：从“看不懂题”到能独立分析常见 Solidity / EVM / DeFi 类 CTF 题。</p>
</blockquote>
<hr/>
<h2>1. CTF 区块链方向学什么？</h2>
<p>CTF 中的区块链题通常不是让你“炒币”或研究公链生态，而是考察：</p>
<ol>
<li>
<p><strong>智能合约基础</strong></p>
<ul>
<li>Solidity 语法</li>
<li>合约部署、调用、转账</li>
<li><code>msg.sender</code>、<code>tx.origin</code>、<code>msg.value</code></li>
<li><code>fallback</code> / <code>receive</code></li>
<li>合约之间如何交互</li>
</ul>
</li>
<li>
<p><strong>EVM 基础</strong></p>
<ul>
<li>以太坊虚拟机如何执行合约</li>
<li>storage / memory / calldata</li>
<li>ABI 编码</li>
<li>函数选择器</li>
<li>gas 的基本概念</li>
</ul>
</li>
<li>
<p><strong>智能合约漏洞</strong></p>
<ul>
<li>重入攻击</li>
<li>整数溢出 / 下溢</li>
<li>权限控制错误</li>
<li>随机数预测</li>
<li><code>delegatecall</code> 滥用</li>
<li><code>tx.origin</code> 钓鱼</li>
<li>selfdestruct 强制转账</li>
<li>storage slot 覆盖</li>
</ul>
</li>
<li>
<p><strong>DeFi 安全基础</strong></p>
<ul>
<li>ERC20 / ERC721</li>
<li>AMM 交易所模型</li>
<li>价格预言机</li>
<li>闪电贷</li>
<li>价格操纵</li>
</ul>
</li>
<li>
<p><strong>链上交互工具</strong></p>
<ul>
<li>Remix</li>
<li>MetaMask</li>
<li>Foundry</li>
<li>Hardhat</li>
<li>Web3.py / ethers.js</li>
</ul>
</li>
</ol>
<hr/>
<h2>2. 推荐学习顺序</h2>
<h3>阶段 0：先补最小必要基础</h3>
<p>如果你是小白，不建议一开始就啃黄皮书或 EVM opcode。先掌握这些：</p>
<ul>
<li>什么是区块链</li>
<li>什么是账户地址</li>
<li>什么是私钥、公钥、签名</li>
<li>什么是交易</li>
<li>什么是智能合约</li>
<li>什么是 gas</li>
<li>什么是以太坊测试网 / 本地链</li>
</ul>
<h4>你需要能回答</h4>
<ul>
<li>合约和普通账户有什么区别？</li>
<li><code>msg.sender</code> 是谁？</li>
<li>向合约转 ETH 会发生什么？</li>
<li>合约能不能主动执行代码？</li>
</ul>
<blockquote>
<p>结论：区块链 CTF 的核心不是“区块链理论”，而是“智能合约代码审计 + 漏洞利用”。</p>
</blockquote>
<hr/>
<h3>阶段 1：学习 Solidity 基础</h3>
<p>先学 Solidity，不要一开始就学太深的 EVM。</p>
<h4>必学语法</h4>
<ul>
<li>变量类型
<ul>
<li><code>uint</code></li>
<li><code>bool</code></li>
<li><code>address</code></li>
<li><code>bytes</code></li>
<li><code>string</code></li>
<li><code>mapping</code></li>
<li><code>array</code></li>
</ul>
</li>
<li>函数可见性
<ul>
<li><code>public</code></li>
<li><code>external</code></li>
<li><code>internal</code></li>
<li><code>private</code></li>
</ul>
</li>
<li>状态变量和局部变量</li>
<li>构造函数 <code>constructor</code></li>
<li>修饰器 <code>modifier</code></li>
<li>继承</li>
<li>事件 <code>event</code></li>
<li>错误处理
<ul>
<li><code>require</code></li>
<li><code>revert</code></li>
<li><code>assert</code></li>
</ul>
</li>
</ul>
<h4>重点理解</h4>
<pre><code>msg.sender
msg.value
tx.origin
address(this).balance
</code></pre>
<p>这些变量在 CTF 题里经常是突破口。</p>
<h4>推荐练习</h4>
<p>用 Remix 写几个小合约：</p>
<ol>
<li>存钱合约</li>
<li>取钱合约</li>
<li>只有 owner 能调用的合约</li>
<li>简单 ERC20 代币</li>
<li>两个合约互相调用</li>
</ol>
<hr/>
<h3>阶段 2：学习基本链上交互</h3>
<p>CTF 题通常会给你一个合约地址、RPC 地址、私钥或网页环境，你需要写脚本调用合约。</p>
<h4>需要掌握的工具</h4>
<table>
<thead>
<tr>
<th>工具</th>
<th>用途</th>
<th>建议程度</th>
</tr>
</thead>
<tbody>
<tr>
<td>Remix</td>
<td>在线写和调试 Solidity</td>
<td>必学</td>
</tr>
<tr>
<td>MetaMask</td>
<td>钱包、签名、切换网络</td>
<td>必学</td>
</tr>
<tr>
<td>Foundry</td>
<td>写 PoC、跑测试、部署合约</td>
<td>强烈推荐</td>
</tr>
<tr>
<td>Hardhat</td>
<td>JS/TS 生态常用开发框架</td>
<td>可选</td>
</tr>
<tr>
<td>Web3.py</td>
<td>Python 调用合约</td>
<td>推荐</td>
</tr>
<tr>
<td>ethers.js</td>
<td>JavaScript 调用合约</td>
<td>推荐</td>
</tr>
</tbody>
</table>
<h4>小白建议</h4>
<p>如果你喜欢 Python：</p>
<pre><code>Solidity + Remix + Web3.py
</code></pre>
<p>如果你想走安全研究 / 审计方向：</p>
<pre><code>Solidity + Foundry
</code></pre>
<p>Foundry 是现在区块链安全题和审计里非常常用的工具。</p>
<hr/>
<h3>阶段 3：学习 EVM 和 ABI 基础</h3>
<p>不要死背 opcode，先掌握 CTF 常用概念。</p>
<h4>必须理解</h4>
<ol>
<li>
<p><strong>ABI 编码</strong></p>
<ul>
<li>函数调用数据如何组成</li>
<li>函数选择器是什么</li>
<li>参数如何编码</li>
</ul>
</li>
<li>
<p><strong>storage / memory / calldata</strong></p>
<ul>
<li><code>storage</code>：永久存储，上链</li>
<li><code>memory</code>：临时内存</li>
<li><code>calldata</code>：外部调用输入数据</li>
</ul>
</li>
<li>
<p><strong>storage slot</strong></p>
<ul>
<li>状态变量如何存在 slot 里</li>
<li><code>private</code> 变量并不是真的私密</li>
<li>mapping 的 slot 如何计算</li>
</ul>
</li>
<li>
<p><strong>合约调用方式</strong></p>
<ul>
<li><code>call</code></li>
<li><code>delegatecall</code></li>
<li><code>staticcall</code></li>
<li><code>transfer</code></li>
<li><code>send</code></li>
</ul>
</li>
</ol>
<h4>CTF 中常见考点</h4>
<ul>
<li>读 private 变量</li>
<li>构造特殊 calldata</li>
<li>绕过函数签名检查</li>
<li>利用 <code>delegatecall</code> 修改调用者 storage</li>
<li>使用合约绕过 <code>isContract</code> 检查</li>
</ul>
<hr/>
<h2>3. 常见漏洞学习路线</h2>
<p>下面这些漏洞建议按顺序学。</p>
<hr/>
<h3>3.1 权限控制漏洞</h3>
<h4>常见问题</h4>
<pre><code>function changeOwner(address newOwner) public {
    owner = newOwner;
}
</code></pre>
<p>没有检查调用者，任何人都能改 owner。</p>
<h4>学习重点</h4>
<ul>
<li><code>onlyOwner</code></li>
<li>初始化函数是否能重复调用</li>
<li>owner 是否可能被覆盖</li>
<li>proxy 合约是否初始化</li>
</ul>
<h4>CTF 常见形式</h4>
<ul>
<li>合约部署后忘记调用初始化</li>
<li>构造函数名字写错，变成普通函数</li>
<li><code>require(tx.origin == owner)</code> 被绕过</li>
</ul>
<hr/>
<h3>3.2 重入攻击 Reentrancy</h3>
<h4>经典场景</h4>
<p>合约先转账，再更新余额：</p>
<pre><code>function withdraw() public {
    uint amount = balances[msg.sender];
    require(amount &gt; 0);

    (bool ok, ) = msg.sender.call{value: amount}("");
    require(ok);

    balances[msg.sender] = 0;
}
</code></pre>
<p>攻击合约在收到 ETH 时再次调用 <code>withdraw()</code>，导致重复取钱。</p>
<h4>学习重点</h4>
<ul>
<li><code>fallback</code> / <code>receive</code></li>
<li>Checks-Effects-Interactions 模式</li>
<li>ReentrancyGuard</li>
<li>跨函数重入</li>
<li>ERC777 hooks 重入</li>
</ul>
<hr/>
<h3>3.3 整数溢出 / 下溢</h3>
<p>Solidity 0.8 以前，整数默认不会自动检查溢出。</p>
<pre><code>uint8 x = 255;
x = x + 1; // 在旧版本中会变成 0
</code></pre>
<h4>学习重点</h4>
<ul>
<li>Solidity 版本差异</li>
<li><code>unchecked</code></li>
<li>SafeMath</li>
<li>token balance 溢出</li>
</ul>
<hr/>
<h3>3.4 随机数预测</h3>
<p>链上数据通常不能安全作为随机数。</p>
<p>危险写法：</p>
<pre><code>uint random = uint(keccak256(abi.encodePacked(block.timestamp, msg.sender))) % 100;
</code></pre>
<h4>学习重点</h4>
<ul>
<li><code>block.timestamp</code> 可被一定程度操控</li>
<li><code>block.number</code> 可预测</li>
<li><code>blockhash</code> 有限制</li>
<li>mempool 中交易可被观察</li>
</ul>
<hr/>
<h3>3.5 <code>tx.origin</code> 漏洞</h3>
<p>不要用 <code>tx.origin</code> 做权限判断。</p>
<p>危险写法：</p>
<pre><code>require(tx.origin == owner);
</code></pre>
<p>攻击者可以诱导 owner 调用攻击合约，攻击合约再调用目标合约，此时 <code>tx.origin</code> 仍然是 owner。</p>
<h4>正确做法</h4>
<pre><code>require(msg.sender == owner);
</code></pre>
<hr/>
<h3>3.6 <code>delegatecall</code> 漏洞</h3>
<p><code>delegatecall</code> 会在调用者的上下文中执行被调用合约代码。</p>
<p>也就是说：</p>
<ul>
<li>代码用的是别人的</li>
<li>storage 改的是自己的</li>
<li><code>msg.sender</code> 不变</li>
<li><code>msg.value</code> 不变</li>
</ul>
<h4>CTF 常见考点</h4>
<ul>
<li>修改 owner</li>
<li>覆盖 storage slot</li>
<li>proxy 初始化漏洞</li>
<li>library 地址被替换</li>
</ul>
<hr/>
<h3>3.7 selfdestruct 强制转账</h3>
<p>即使目标合约没有 <code>receive()</code>，攻击者也可能通过 <code>selfdestruct</code> 强制给它转 ETH。</p>
<h4>CTF 常见考点</h4>
<pre><code>require(address(this).balance == 0);
</code></pre>
<p>这类判断可能被强制转账破坏。</p>
<hr/>
<h3>3.8 Private 不等于秘密</h3>
<p>Solidity 里的 <code>private</code> 只是不允许其他合约直接访问，不代表链上数据不可见。</p>
<pre><code>bytes32 private password;
</code></pre>
<p>这个 <code>password</code> 仍然可以通过读取 storage slot 得到。</p>
<hr/>
<h2>4. 推荐靶场和题单</h2>
<h3>入门靶场</h3>
<ol>
<li>
<p><strong>Ethernaut</strong></p>
<ul>
<li>地址：<a href="https://ethernaut.openzeppelin.com/" rel="noopener nofollow" target="_blank">https://ethernaut.openzeppelin.com/</a></li>
<li>最经典的 Solidity 安全入门靶场</li>
<li>建议完整刷一遍</li>
</ul>
</li>
<li>
<p><strong>Damn Vulnerable DeFi</strong></p>
<ul>
<li>地址：<a href="https://www.damnvulnerabledefi.xyz/" rel="noopener nofollow" target="_blank">https://www.damnvulnerabledefi.xyz/</a></li>
<li>DeFi 安全经典练习</li>
<li>适合学完基础漏洞后刷</li>
</ul>
</li>
<li>
<p><strong>Capture the Ether</strong></p>
<ul>
<li>地址：<a href="https://capturetheether.com/" rel="noopener nofollow" target="_blank">https://capturetheether.com/</a></li>
<li>早期经典区块链 CTF 靶场</li>
</ul>
</li>
<li>
<p><strong>Paradigm CTF</strong></p>
<ul>
<li>地址：<a href="https://github.com/paradigmxyz/paradigm-ctf-2021" rel="noopener nofollow" target="_blank">https://github.com/paradigmxyz/paradigm-ctf-2021</a></li>
<li>难度较高，适合进阶</li>
</ul>
</li>
<li>
<p><strong>QuillCTF</strong></p>
<ul>
<li>地址：<a href="https://quillctf.super.site/" rel="noopener nofollow" target="_blank">https://quillctf.super.site/</a></li>
<li>智能合约安全练习题</li>
</ul>
</li>
</ol>
<hr/>
<h2>5. 建议学习路线图</h2>
<h3>第 1 周：建立基本概念</h3>
<p>目标：看懂最简单的合约。</p>
<p>任务：</p>
<ul>
<li>了解以太坊账户、交易、gas</li>
<li>学 Solidity 基础语法</li>
<li>用 Remix 部署一个 HelloWorld 合约</li>
<li>写一个存钱 / 取钱合约</li>
<li>理解 <code>msg.sender</code> 和 <code>msg.value</code></li>
</ul>
<p>练习：</p>
<ul>
<li>Remix 部署合约</li>
<li>调用合约函数</li>
<li>给合约转 ETH</li>
</ul>
<hr/>
<h3>第 2 周：掌握合约交互</h3>
<p>目标：能写攻击合约。</p>
<p>任务：</p>
<ul>
<li>学习合约之间调用</li>
<li>学习 <code>receive()</code> 和 <code>fallback()</code></li>
<li>学习 ABI 和函数选择器</li>
<li>用 Web3.py 或 Foundry 调用合约</li>
</ul>
<p>练习：</p>
<ul>
<li>写一个合约调用另一个合约</li>
<li>写一个攻击合约触发 fallback</li>
<li>计算函数选择器</li>
</ul>
<hr/>
<h3>第 3 周：刷 Ethernaut</h3>
<p>目标：掌握常见 CTF 基础漏洞。</p>
<p>推荐顺序：</p>
<ol>
<li>Hello Ethernaut</li>
<li>Fallback</li>
<li>Fallout</li>
<li>Coin Flip</li>
<li>Telephone</li>
<li>Token</li>
<li>Delegation</li>
<li>Force</li>
<li>Vault</li>
<li>King</li>
<li>Re-entrancy</li>
<li>Elevator</li>
<li>Privacy</li>
<li>Gatekeeper One</li>
<li>Gatekeeper Two</li>
<li>Preservation</li>
</ol>
<p>每题都要整理：</p>
<pre><code>## 题目名

### 漏洞点

### 利用思路

### 关键代码

### 学到的知识
</code></pre>
<hr/>
<h3>第 4 周：学习 Foundry</h3>
<p>目标：能本地复现和写 PoC。</p>
<p>任务：</p>
<ul>
<li>安装 Foundry</li>
<li>学会 <code>forge init</code></li>
<li>学会 <code>forge test</code></li>
<li>学会写 Solidity 测试</li>
<li>学会 <code>vm.prank</code></li>
<li>学会 <code>deal</code></li>
<li>学会 fork 主网 / 测试网</li>
</ul>
<p>常用命令：</p>
<pre><code>forge init demo
forge build
forge test -vvv
cast call &lt;address&gt; &lt;function-signature&gt;
cast send &lt;address&gt; &lt;function-signature&gt; --private-key &lt;key&gt;
cast storage &lt;address&gt; &lt;slot&gt;
</code></pre>
<hr/>
<h3>第 5 周：进入 DeFi 安全</h3>
<p>目标：能看懂简单 DeFi 题。</p>
<p>任务：</p>
<ul>
<li>学 ERC20</li>
<li>学 AMM 模型</li>
<li>理解恒定乘积公式 <code>x * y = k</code></li>
<li>理解价格预言机</li>
<li>理解闪电贷</li>
</ul>
<p>练习：</p>
<ul>
<li>Damn Vulnerable DeFi 前几题</li>
<li>简单 Uniswap V2 模型题</li>
</ul>
<hr/>
<h2>6. CTF 做题基本流程</h2>
<p>拿到一道区块链题后，按这个流程分析。</p>
<h3>第一步：读题目目标</h3>
<p>常见目标：</p>
<ul>
<li>让 <code>isSolved()</code> 返回 true</li>
<li>把合约余额清空</li>
<li>成为 owner</li>
<li>获得某个 token</li>
<li>让某个状态变量改变</li>
</ul>
<p>先找类似代码：</p>
<pre><code>function isSolved() public view returns (bool) {
    return ...;
}
</code></pre>
<hr/>
<h3>第二步：看合约版本</h3>
<pre><code>pragma solidity ^0.6.0;
pragma solidity ^0.8.0;
</code></pre>
<p>重点：</p>
<ul>
<li>Solidity &lt; 0.8 可能有整数溢出</li>
<li>老版本构造函数、fallback 写法不同</li>
<li>ABIEncoderV2 在老版本中可能有历史问题</li>
</ul>
<hr/>
<h3>第三步：找资产和权限</h3>
<p>重点看：</p>
<pre><code>owner
admin
balance
balances
token
withdraw
transfer
approve
</code></pre>
<p>思考：</p>
<ul>
<li>谁能取钱？</li>
<li>谁能改 owner？</li>
<li>是否有初始化函数？</li>
<li>是否有权限检查遗漏？</li>
</ul>
<hr/>
<h3>第四步：看外部调用</h3>
<p>重点找：</p>
<pre><code>call
delegatecall
send
transfer
approve
transferFrom
onERC721Received
onERC1155Received
</code></pre>
<p>思考：</p>
<ul>
<li>是否先转账后改状态？</li>
<li>是否可重入？</li>
<li>是否能调用恶意合约？</li>
<li><code>delegatecall</code> 是否能改 storage？</li>
</ul>
<hr/>
<h3>第五步：看随机数和时间</h3>
<p>重点找：</p>
<pre><code>block.timestamp
block.number
blockhash
keccak256
</code></pre>
<p>思考：</p>
<ul>
<li>随机数是否可预测？</li>
<li>是否可以在同一笔交易中算出结果？</li>
</ul>
<hr/>
<h3>第六步：写 PoC</h3>
<p>常见 PoC 方式：</p>
<ol>
<li>Remix 手动调用</li>
<li>Foundry 写测试</li>
<li>Web3.py 写脚本</li>
<li>ethers.js 写脚本</li>
</ol>
<p>建议优先用 Foundry，因为很多区块链 CTF 题可以直接写 Solidity 攻击合约和测试。</p>
<hr/>
<h2>7. 常用检查清单</h2>
<p>做题时可以逐项检查。</p>
<h3>权限类</h3>
<ul>
<li><input disabled="" type="checkbox"/><label> 是否有 <code>onlyOwner</code>？</label></li>
<li><input disabled="" type="checkbox"/><label> owner 是否可被改？</label></li>
<li><input disabled="" type="checkbox"/><label> 初始化函数是否可重复调用？</label></li>
<li><input disabled="" type="checkbox"/><label> 是否错误使用 <code>tx.origin</code>？</label></li>
<li><input disabled="" type="checkbox"/><label> 是否存在未保护的 <code>delegatecall</code>？</label></li>
</ul>
<h3>资金类</h3>
<ul>
<li><input disabled="" type="checkbox"/><label> 是否先转账后更新余额？</label></li>
<li><input disabled="" type="checkbox"/><label> 是否能重入？</label></li>
<li><input disabled="" type="checkbox"/><label> 是否能强制转 ETH？</label></li>
<li><input disabled="" type="checkbox"/><label> 是否依赖 <code>address(this).balance</code> 做关键判断？</label></li>
<li><input disabled="" type="checkbox"/><label> 是否有整数溢出 / 下溢？</label></li>
</ul>
<h3>数据类</h3>
<ul>
<li><input disabled="" type="checkbox"/><label> private 变量是否可从 storage 读取？</label></li>
<li><input disabled="" type="checkbox"/><label> mapping slot 是否可计算？</label></li>
<li><input disabled="" type="checkbox"/><label> calldata 是否可伪造？</label></li>
<li><input disabled="" type="checkbox"/><label> ABI 编码是否有特殊点？</label></li>
</ul>
<h3>DeFi 类</h3>
<ul>
<li><input disabled="" type="checkbox"/><label> 价格是否来自单一池子？</label></li>
<li><input disabled="" type="checkbox"/><label> 是否可通过闪电贷操纵价格？</label></li>
<li><input disabled="" type="checkbox"/><label> 是否检查滑点？</label></li>
<li><input disabled="" type="checkbox"/><label> 是否存在精度损失？</label></li>
<li><input disabled="" type="checkbox"/><label> 是否有 share / token 兑换比例问题？</label></li>
</ul>
<hr/>
<h2>8. 小白最容易踩的坑</h2>
<h3>只看 Solidity，不看交易流程</h3>
<p>很多题的关键不在单个函数，而在调用顺序。</p>
<p>例如：</p>
<ol>
<li>先部署攻击合约</li>
<li>调用目标合约</li>
<li>目标合约回调攻击合约</li>
<li>攻击合约再次调用目标合约</li>
</ol>
<hr/>
<h3>以为 private 真的是私密</h3>
<p>链上所有 storage 都可以被节点读取。</p>
<hr/>
<h3>不理解 msg.sender</h3>
<p>如果 A 调用 B，B 里看到的 <code>msg.sender</code> 是 A。<br/>
如果用户调用攻击合约 A，A 再调用目标 B，B 里看到的 <code>msg.sender</code> 是 A，不是用户。</p>
<hr/>
<h3>不会写攻击合约</h3>
<p>很多题不能只靠手动点 Remix，需要写一个中间攻击合约。</p>
<hr/>
<h3>没有本地复现</h3>
<p>建议所有题都尽量本地写测试复现。只看 writeup 很容易以为自己懂了。</p>
<hr/>
<h2>9. 推荐工具安装</h2>
<h3>Foundry</h3>
<p>官网：<a href="https://book.getfoundry.sh/" rel="noopener nofollow" target="_blank">https://book.getfoundry.sh/</a></p>
<p>安装后常用：</p>
<pre><code>forge --version
cast --version
anvil --version
</code></pre>
<p>工具作用：</p>
<ul>
<li><code>forge</code>：编译、测试 Solidity 项目</li>
<li><code>cast</code>：命令行调用链上合约</li>
<li><code>anvil</code>：本地区块链节点</li>
</ul>
<hr/>
<h3>Node.js + Hardhat</h3>
<p>适合 JS/TS 生态。</p>
<pre><code>npm install --save-dev hardhat
npx hardhat init
npx hardhat test
</code></pre>
<hr/>
<h3>Python + Web3.py</h3>
<p>适合喜欢 Python 的同学。</p>
<pre><code>pip install web3
</code></pre>
<p>简单调用示例：</p>
<pre><code>from web3 import Web3

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
print(w3.is_connected())
</code></pre>
<hr/>
<h2>10. 推荐资料</h2>
<h3>官方文档</h3>
<ul>
<li>Solidity 文档：<a href="https://docs.soliditylang.org/" rel="noopener nofollow" target="_blank">https://docs.soliditylang.org/</a></li>
<li>Foundry 文档：<a href="https://book.getfoundry.sh/" rel="noopener nofollow" target="_blank">https://book.getfoundry.sh/</a></li>
<li>OpenZeppelin 文档：<a href="https://docs.openzeppelin.com/" rel="noopener nofollow" target="_blank">https://docs.openzeppelin.com/</a></li>
<li>Ethereum Developer Docs：<a href="https://ethereum.org/developers/" rel="noopener nofollow" target="_blank">https://ethereum.org/developers/</a></li>
</ul>
<h3>靶场</h3>
<ul>
<li>Ethernaut：<a href="https://ethernaut.openzeppelin.com/" rel="noopener nofollow" target="_blank">https://ethernaut.openzeppelin.com/</a></li>
<li>Damn Vulnerable DeFi：<a href="https://www.damnvulnerabledefi.xyz/" rel="noopener nofollow" target="_blank">https://www.damnvulnerabledefi.xyz/</a></li>
<li>Capture the Ether：<a href="https://capturetheether.com/" rel="noopener nofollow" target="_blank">https://capturetheether.com/</a></li>
<li>Paradigm CTF：<a href="https://github.com/paradigmxyz/paradigm-ctf-2021" rel="noopener nofollow" target="_blank">https://github.com/paradigmxyz/paradigm-ctf-2021</a></li>
</ul>
<h3>安全参考</h3>
<ul>
<li>SWC Registry：<a href="https://swcregistry.io/" rel="noopener nofollow" target="_blank">https://swcregistry.io/</a></li>
<li>ConsenSys Smart Contract Best Practices：<a href="https://consensys.github.io/smart-contract-best-practices/" rel="noopener nofollow" target="_blank">https://consensys.github.io/smart-contract-best-practices/</a></li>
<li>OpenZeppelin Blog：<a href="https://blog.openzeppelin.com/" rel="noopener nofollow" target="_blank">https://blog.openzeppelin.com/</a></li>
</ul>
<hr/>
<h2>11. 建议的学习方式</h2>
<p>不要只看教程，建议用下面这个循环：</p>
<pre><code>学一个概念
  ↓
看一个简单漏洞例子
  ↓
自己写一遍漏洞合约
  ↓
自己写攻击合约
  ↓
用 Foundry 或 Remix 复现
  ↓
刷一道对应 CTF 题
  ↓
写笔记总结
</code></pre>
<p>每道题至少总结四点：</p>
<pre><code># 题目名

## 目标

题目要求我做到什么？

## 漏洞

合约哪里写错了？

## 利用

我如何利用这个错误？

## 修复

真实项目里应该怎么修？
</code></pre>
<hr/>
<h2>12. 最小可行学习路线</h2>
<p>如果你时间有限，按这个路线走：</p>
<pre><code>Solidity 基础
  ↓
Remix 部署和调用合约
  ↓
msg.sender / msg.value / fallback / receive
  ↓
Ethernaut 前 15 题
  ↓
Foundry 基础
  ↓
重入、delegatecall、storage、ABI
  ↓
Damn Vulnerable DeFi 入门题
</code></pre>
<hr/>
<h2>13. 学到什么程度算入门？</h2>
<p>如果你能做到下面这些，就算区块链 CTF 入门了：</p>
<ul>
<li>能看懂普通 Solidity 合约</li>
<li>能判断谁能调用某个函数</li>
<li>能写简单攻击合约</li>
<li>能解释重入攻击</li>
<li>能读 storage slot</li>
<li>能用 Remix 或 Foundry 复现漏洞</li>
<li>能独立完成 Ethernaut 前 10~15 题</li>
<li>能根据 <code>isSolved()</code> 反推解题目标</li>
</ul>
<hr/>
<h2>14. 后续进阶方向</h2>
<p>入门后可以继续学：</p>
<ol>
<li>
<p><strong>EVM opcode</strong></p>
<ul>
<li>反编译合约</li>
<li>字节码分析</li>
<li>gas 优化题</li>
</ul>
</li>
<li>
<p><strong>Proxy 和升级合约</strong></p>
<ul>
<li>Transparent Proxy</li>
<li>UUPS</li>
<li>storage collision</li>
</ul>
</li>
<li>
<p><strong>DeFi 攻击</strong></p>
<ul>
<li>闪电贷</li>
<li>价格操纵</li>
<li>oracle attack</li>
<li>sandwich attack</li>
<li>MEV 基础</li>
</ul>
</li>
<li>
<p><strong>形式化验证和审计工具</strong></p>
<ul>
<li>Slither</li>
<li>Mythril</li>
<li>Echidna</li>
<li>Foundry fuzzing</li>
</ul>
</li>
<li>
<p><strong>真实链上攻击复盘</strong></p>
<ul>
<li>The DAO</li>
<li>bZx</li>
<li>Harvest Finance</li>
<li>Euler Finance</li>
<li>Curve / Vyper 事件</li>
</ul>
</li>
</ol>
<hr/>
<h2>15. 给小白的一句话建议</h2>
<p>区块链 CTF 不要一开始追求“看懂所有 EVM 细节”。</p>
<p>最有效的入门方式是：</p>
<blockquote>
<p>先学 Solidity，刷 Ethernaut，边刷边补 EVM 和 Foundry。</p>
</blockquote>
<p>遇到题目时重点问自己三件事：</p>
<ol>
<li>题目最终要我改变什么状态？</li>
<li>哪个函数能影响这个状态？</li>
<li>我能不能用合约调用、重入、delegatecall、storage、ABI 等方式绕过限制？</li>
</ol>
<p>只要坚持复现和写 PoC，进步会非常快。</p>
