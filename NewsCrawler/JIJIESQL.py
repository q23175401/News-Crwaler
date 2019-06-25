import pymysql


class JIJIESQLDB:
    def __init__(self):
        self.conn = pymysql.connect(host='127.0.0.1',
                                    port=3306,
                                    user='root',
                                    passwd='*********',
                                    db='JIJIESQL',
                                    charset='utf8',
                                    cursorclass=pymysql.cursors.DictCursor)
        print("建立連線")
        self.cur = self.conn.cursor()

    # #effect_row = cursor.executemany("insert into tb7(user,pass,licnese)values(%s,%s,%s)", [("u1","u1pass","11111"),("u2","u2pass","22222")])

    def insert_news(self, news):
        sql = "INSERT INTO news(news_id, news_url, news_title, news_content) \
               VALUES (\"{}\", \"{}\", \"{}\", \"{}\")".format(
            news['news_id'],
            news['news_url'],
            news['news_title'],
            news['news_content'],
        )
        try:
            self.cur.execute(sql)
            self.conn.commit()
        except pymysql.OperationalError:
            print('Error! Insert new list error!')
            return False

        return True

    def select_all(self):
        sql = "SELECT * FROM news"
        try:
            self.cur.execute(sql)
            rows = self.cur.fetchall()
            self.conn.commit()
        except pymysql.OperationalError:
            print('Error! Insert new list error!')

        # for r in content:
            # print(r)

        return rows

    def delete_all(self):
        delete = "DELETE FROM news"
        auto = "ALTER TABLE news AUTO_INCREMENT=0"
        try:
            self.cur.execute(delete)
            self.cur.execute(auto)
            self.conn.commit()

        except pymysql.OperationalError:
            print('Error! Insert new list error!')

    def __del__(self):
        print("關閉連線")
        self.cur.close()
        self.conn.close()

    def select_all_one_by_one(self):
        sql = "SELECT * FROM news"
        try:
            self.cur.execute(sql)
            # one_row = self.cur.fetchone()
            self.conn.commit()
        except pymysql.OperationalError:
            print('Error! Insert new list error!')
        # for r in content:
            # print(r)
        # print(one_row['news_content'])
        while True:
            try:
                one_row = self.cur.fetchone()
                yield one_row
            except:
                raise StopIteration

    def select_one_by_id(self, id):
        sql = "SELECT * FROM news WHERE news_id = \"{}\"".format(id)
        try:
            self.cur.execute(sql)
            one_row = self.cur.fetchone()
            self.conn.commit()
        except pymysql.OperationalError:
            print('Error! select one error!')
        return one_row

    def select_by_data_id_list(self, ids):
        select_id_string = ", ".join(ids)
        sql = "SELECT * FROM news WHERE id IN ({})".format(select_id_string)
        try:
            self.cur.execute(sql)
            all_news = self.cur.fetchall()
            self.conn.commit()
        except pymysql.OperationalError:
            print('Error! select list error!')
        return all_news

    def select_by_new_id_list(self, news_ids):
        select_newid_string = "\"" + "\", \"".join(news_ids) + "\""
        sql = "SELECT * FROM news WHERE news_id IN ({})".format(select_newid_string)
        try:
            self.cur.execute(sql)
            all_news = self.cur.fetchall()
            self.conn.commit()
        except pymysql.OperationalError:
            print('Error! select list error!')
        return all_news

    def select_all_and_generate_dict(self):
        sql = "SELECT * FROM news"
        try:
            self.cur.execute(sql)
            all_news = self.cur.fetchall()
            self.conn.commit()
        except pymysql.OperationalError:
            print('Error! Insert new list error!')
        dict = {}
        for row in all_news:
            dict[row['news_id']] = row
        return dict


if __name__ == "__main__":
    news_dict = {
        'news_id': 'new_1',
        'news_url': "https:\\apple.com",
        'news_title': "你很醜",
        'news_content': "你真的超級醜"
    }
    db = JIJIESQLDB()
    all_row = select_all_one_by_one()
    print(all_row)

