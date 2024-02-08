from whoosh.fields import Schema, TEXT, ID, DATETIME
import os
from flask import current_app
from whoosh.index import open_dir,create_in, exists_in
from whoosh.writing import AsyncWriter
from whoosh.qparser import QueryParser

class Search:
    def __init__(self):
        self.index_path = "1"
        self.app = None
    def add_to_search_index(self, post_id, slug, title, publish_date,summary,thumbnail):
        print(self.index_path)
        ix = open_dir(self.index_path)
        writer = AsyncWriter(ix)
        writer.add_document(
            id=str(post_id),
            slug=slug,
            title=title,
            summary=summary,
            publish_date=publish_date,
            thumbnail=thumbnail
        )
        
        writer.commit()

    def search_posts(self, query_str):
        index = open_dir(self.index_path)
        with index.searcher() as searcher:
            query = QueryParser("title", index.schema).parse(query_str)
            results_obj = searcher.search(query)
            query_results = []
            for hit in results_obj:
                h = {
                    'id':hit['id'],
                    'title':hit['title'],
                    'slug':hit['slug'],
                    'publish_date': hit['publish_date'],
                    'summary': hit['summary'],
                    'thumbnail': hit['thumbnail']
                }
                query_results.append(h)
            return query_results

    def remove_from_search_index(self, id):
        ix = open_dir(self.index_path)
        writer = AsyncWriter(ix)
        writer.delete_by_term('id', str(id))
        writer.commit()


    def init_app(self, app):
        schema = Schema(
        id=ID(unique=True, stored=True),
        slug=TEXT(stored=True),
        title=TEXT(stored=True),
        summary=TEXT(stored=True),
        thumbnail=TEXT(stored=True),
        publish_date=TEXT(stored=True)
        )

        index_path = f'{app.instance_path}/search_index'
        self.index_path = index_path
        self.app = app
        self.app.wc_search = self
        if not os.path.exists(index_path):
            os.makedirs(index_path)
        if not exists_in(index_path):
            create_in(index_path, schema)
