Language="Zh_cn"
texts={
    "Zh_cn":[
        "题目未找到。",
        "题号",
        "注意",
        "此题目不支持使用Python",
        "缺少参数",
        "设置语言。",
        "选项。",
        "题目编号。",
        "作者。",
        "当前文件夹已经是N0Code工作区了。",
        "错误",
        "初始化完成。享受算法吧 :)",
        "当前文件夹不是一个N0Code工作区.请执行'N0Code.py init'。",
        " 未找到。",
        " 无法被访问。",
        "问题编号必须是一个整数。",
        "例",
        "描述",
        "标题",
        "恭喜！你已经完成了所有的题目。",
        "请执行'pip install lxml'"
    ]
}
main_text=[
    "Problem not found.",
    "QuestionId",
    "Notice",
    "This problem does not support using python",
    "Lack of parameter",
    "Set language.",
    "Option.",
    "Question Id.",
    "Author.",
    "The current folder is already a N0Code-workspace.",
    "Error",
    "Initialization is complete.Enjoy your algorithm :)",
    "The current folder is not a N0Code-workspace.Please run 'N0Code.py init'.",
    " Not Found.",
    " Can't be accessed.",
    "Question Id must be an integer.",
    "Example",
    "Description",
    "Title",
    "Congratulations! You have already finished all the questions.",
    "Please run 'pip install lxml"
    
]
def I18n(text):
    try: 
        return texts[Language][main_text.index(text)]
    except:
        return text