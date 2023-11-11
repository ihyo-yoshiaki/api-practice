import datetime as dt
import arxiv

# （参考1：論文要約プログラム）https://qiita.com/yuta0821/items/2edf338a92b8a157af37
# （参考2：arxiv api）https://qiita.com/KMD/items/bd59f2db778dd4bf6ed2 
#       

# -- tmporary variable -- #
N_DAYS = 7
keyword = None
MAX_RESULT = 10
# ----------------------- #

class SearchArxiv:
    query_prameter = [
        "search_query"#string None No
        "id_list"   #comma-delimited string None No
        "start"     #int 0	
        "max_results" #int 10
    ]
    query_prefix = [
        "ti"    #タイトル(Title)
        "au"    #著作者(Author)
        "abs"   #概要(Abstract)
        "co"    #コメント(Comment)
        "jr"    #雑誌名(Journal Reference)
        "cat"   #サブジャンルカテゴリー(Subject Category)
        "rn"    #Report Number
        "id"    #Id (use id_list instead)
        "all"
    ]
    query_logical = {
        "and": "AND",
        "or" : "OR",
        "andnot": "ANDNOT",
    }
    sortBy = {
        "relevance": arxiv.SortCriterion.Relevance,
        "lastUpdateDate": arxiv.SortCriterion.LastUpdatedDate,
        "submittedDate": arxiv.SortCriterion.SubmittedDate,
    }
    sortOrder = {
        "descending": arxiv.SortOrder.Descending,
        "ascending": arxiv.SortOrder.Descending,
    }
    
    paper_content = [
        "author",
        "link",
        "title",
        "published",
        "summary",
        "category",
    ]
    
    def __init__(self) -> None:
        pass

    def make_query(self) -> str:
        head = "http://export.arxiv.org/api/query?search_query="

# テンプレートを用意
QUERY_TEMPLATE = '%28 ti:%22{}%22 OR abs:%22{}%22 %29 AND submittedDate: [{} TO {}]'

# arXivの更新頻度を加味して，1週間前の論文を検索
today = dt.datetime.today() - dt.timedelta(days=7)
base_date = today - dt.timedelta(days=N_DAYS)
query = QUERY_TEMPLATE.format(keyword, keyword, base_date.strftime("%Y%m%d%H%M%S"), today.strftime("%Y%m%d%H%M%S"))

search = arxiv.Search(
    query=query,  # 検索クエリ
    max_results=MAX_RESULT * 3,  # 取得する論文数の上限
    sort_by=arxiv.SortCriterion.SubmittedDate,  # 論文を投稿された日付でソートする
    sort_order=arxiv.SortOrder.Descending,  # 新しい論文から順に取得する
)

# 興味があるカテゴリー群
CATEGORIES = {
    "cs.AI",
}

# searchの結果をリストに格納
result_list = []
for result in search.results():
    # カテゴリーに含まれない論文は除く
    if len((set(result.categories) & CATEGORIES)) == 0:
        continue
    result_list.append(result)
    
print(result_list[0].keys())

