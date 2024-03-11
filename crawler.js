import axios from "axios";
import * as cheerio from "cheerio";

const url = `https://sedaily.com/NewsList/GB07`; // 일반 뉴스

const getNewsData = async () => {
  try {
    const html = await axios.get(url);
    const $ = cheerio.load(html.data);
    const newList = $(".sub_news_list li");

    newList.map((i, el) => {
      newList[i] = {
        id: i + 1,
        title: $(el).find(".article_tit").text().replace(/\s/g, ""),
        date: $(el).find(".text_info .date").text().replace(/\s/g, ""),
        thumb: $(el).find(".thumb img").attr("src"),
        link: $(el).find("a").attr("href"),
      };
    });

    console.log("newList", newList);
  } catch (err) {
    console.error(err);
  }
};

getNewsData();
