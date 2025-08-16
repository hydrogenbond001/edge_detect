import os
import re
import pdfplumber
import pandas as pd

# === 配置 ===
pdf_folder = r"C:\Users\L3101\Desktop\工训国赛剩余发票"     # 发票文件夹
output_excel = r"C:\Users\L3101\Desktop\工训国赛剩余发票.xlsx"

money_re = re.compile(r"[¥￥]?\s*([0-9]{1,3}(?:,[0-9]{3})*(?:\.\d+)?)")

def norm_num(s):
    return float(s.replace(',', '').replace('¥','').replace('￥','').strip())

def find_money_in_line(line):
    return [norm_num(m) for m in money_re.findall(line)]

def find_bottom_totals(text):
    # 从底部向上找包含合计/价税合计/小写的行
    lines = [l.rstrip() for l in text.splitlines() if l.strip()]
    for i in range(len(lines)-1, -1, -1):
        ln = lines[i]
        if any(k in ln for k in ("价税合计", "小写", "合计")):
            nums = find_money_in_line(ln)
            if nums:
                return nums, ln, i
    return [], "", -1

def find_tax_amount(text):
    # 从底部向上找“税额”行
    lines = [l.rstrip() for l in text.splitlines() if l.strip()]
    for ln in reversed(lines):
        if "税额" in ln:
            nums = find_money_in_line(ln)
            if nums:
                return nums[0], ln
    return None, None

rows = []
for fname in os.listdir(pdf_folder):
    if not fname.lower().endswith(".pdf"):
        continue
    path = os.path.join(pdf_folder, fname)
    with pdfplumber.open(path) as pdf:
        text = ""
        for p in pdf.pages:
            t = p.extract_text() or ""
            text += t + "\n"

    # 先尝试从底部合计行解析
    nums, line_text, line_idx = find_bottom_totals(text)
    tax_exclusive = tax = total = None

    if nums:
        # 常见情况：合计行包含两个数（不含税、税额），或只包含总额（小写）
        if len(nums) >= 2:
            tax_exclusive = round(nums[0], 2)
            tax = round(nums[1], 2)
            total = round(tax_exclusive + tax, 2)
        else:
            # 只有一个数，可能是总额（小写），我们再找税额
            total = round(nums[0], 2)
            tax_val, _ = find_tax_amount(text)
            if tax_val is not None:
                tax = round(tax_val, 2)
                tax_exclusive = round(total - tax, 2)
    else:
        # 回退策略：找“金额/税额/价税合计”通用正则（适配各种格式）
        m_pre = re.search(r"(?:不含税金额|金额)[:：]?\s*[¥￥]?\s*([0-9,]+\.\d+)", text)
        m_tax = re.search(r"(?:税额|税费)[:：]?\s*[¥￥]?\s*([0-9,]+\.\d+)", text)
        m_total = re.search(r"(?:价税合计|合计(?:\s*（小写）)?)[:：]?\s*[¥￥]?\s*([0-9,]+\.\d+)", text)
        if m_pre:
            tax_exclusive = round(norm_num(m_pre.group(1)), 2)
        if m_tax:
            tax = round(norm_num(m_tax.group(1)), 2)
        if m_total:
            total = round(norm_num(m_total.group(1)), 2)
        # 若缺某项，尝试计算
        if tax_exclusive is None and total is not None and tax is not None:
            tax_exclusive = round(total - tax, 2)
        if total is None and tax_exclusive is not None and tax is not None:
            total = round(tax_exclusive + tax, 2)

    # debug：如果任一值缺失或不一致，打印上下文便于调试
    if tax_exclusive is None or tax is None or total is None or abs((tax_exclusive + tax) - total) > 0.01:
        print(f"[WARN] {fname} 解析疑似异常：")
        print(" 合计行索引:", line_idx, " 合计行内容:", line_text)
        print(" 提取到的 nums:", nums)
        print(" 预估: 不含税=", tax_exclusive, " 税额=", tax, " 总额=", total)
        # 可打印片段查看文本上下文
        lines = text.splitlines()
        for idx in range(max(0, line_idx-3), min(len(lines), line_idx+4)):
            print(f" L{idx}: {lines[idx]}")
        print("-"*60)

    rows.append({
        "文件名": fname,
        "税前金额": tax_exclusive if tax_exclusive is not None else 0.0,
        "税额": tax if tax is not None else 0.0,
        "总金额": total if total is not None else 0.0
    })

df = pd.DataFrame(rows)
# 汇总行
sum_row = {"文件名":"合计", "税前金额": df["税前金额"].sum(), "税额": df["税额"].sum(), "总金额": df["总金额"].sum()}
df = pd.concat([df, pd.DataFrame([sum_row])], ignore_index=True)
df.to_excel(output_excel, index=False)
print("完成，保存到", output_excel)
