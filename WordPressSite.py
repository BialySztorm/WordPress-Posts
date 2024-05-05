from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost
from wordpress_xmlrpc.methods.taxonomies import GetTerms, NewTerm
from wordpress_xmlrpc import WordPressTerm
from os import path


class WordPressSite:
    def __init__(self):
        with open(".env", "r") as file:
            self.url = file.readline().strip()
            self.username = file.readline().strip()
            self.password = file.readline().strip()
        self.wp = Client(self.url, self.username, self.password)

    def create_post(self, post_title, post_content, categories=[], tags=[], post_url=""):
        post = WordPressPost()
        post.title = post_title
        post.content = post_content
        post.post_status = 'publish'
        if (post_url != ""):
            post.slug = post_url
        post.terms_names = {
            'category': categories,
            'post_tag': tags
        }
        self.create_category_if_not_exists(categories)
        self.create_tag_if_not_exists(tags)
        post.id = self.wp.call(NewPost(post))
        return post.id

    def get_categories(self):
        categories = self.wp.call(GetTerms('category'))
        return [category.name for category in categories]

    def get_tags(self):
        tags = self.wp.call(GetTerms('post_tag'))
        return [tag.name for tag in tags]

    def create_category_if_not_exists(self, categories):
        tmp_categories = self.get_categories()
        for category in categories:
            if category not in tmp_categories:
                tag = WordPressTerm()
                tag.taxonomy = 'category'
                tag.name = category
                self.wp.call(NewTerm(tag))

    def create_tag_if_not_exists(self, tags):
        tmp_tags = self.get_tags()
        for tag_name in tags:
            if tag_name not in tmp_tags:
                tag = WordPressTerm()
                tag.taxonomy = 'post_tag'
                tag.name = tag_name
                self.wp.call(NewTerm(tag))
