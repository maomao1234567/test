# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from ..items import Cloud163Item
import time


class MusicSpider(scrapy.Spider):
    name = 'music'
    base_url = 'https://music.163.com'
    ids = ['1001','1002']
    initials = [i for i in range(65, 80)]+[0]

    def start_requests(self):
        for id in self.ids:
            for initial in self.initials:
                url = '{url}/discover/artist/cat?id={id}&initial={initial}'.format(url=self.base_url,id=id,initial=initial)
                yield Request(url, callback=self.parse_index)

    # 获得所有歌手的url
    def parse_index(self, response):
         for sel in response.xpath('//*[@id="m-artist-box"]/li/*'):     #网易云音乐的歌手页有两个组成部分，上方十个带头像的热门歌手和下方只显示姓名的普通歌手，原来的xpath选择器只能得到热门歌手id,现已修改
             artist=sel.re('href\=\"\/artist\?id\=[(0-9)]{4,9}')
             for artistid in artist:
                 artist_url = self.base_url + '/artist' + '/album?' + artistid[14:]
                 yield Request(artist_url, callback=self.parse_artist_pre)

    def parse_artist_pre(self,response):
        artist_albums=response.xpath('//*[@class="u-page"]/a[@class="zpgi"]/@href').extract()       #得到专辑页的翻页html elements列表
        if artist_albums==[]:       #若为空，说明只有一页，即套用原parse_artist方法的代码，注意callback=self.parse_album
            albums = response.xpath('//*[@id="m-song-module"]/li/div/a[@class="msk"]/@href').extract()
            for album in albums:
                album_url = self.base_url + album
                yield Request(album_url, callback=self.parse_album)
        else:       #若不为空，即该歌手专辑存在分页，那么得到分页的url，注意callback=self.parse_artist
            for artist_album in artist_albums:
                artist_album_url = self.base_url + artist_album
                yield Request(artist_album_url, callback=self.parse_artist)

    # 获得所有歌手专辑的url
    def parse_artist(self, response):
        albums = response.xpath('//*[@id="m-song-module"]/li/div/a[@class="msk"]/@href').extract()
        for album in albums:
            album_url = self.base_url + album
            yield Request(album_url, callback=self.parse_album)

    # 获得所有专辑音乐的url
    def parse_album(self, response):
        musics = response.xpath('//ul[@class="f-hide"]/li/a/@href').extract()
        for music in musics:
            music_id = music[9:]
            music_url = self.base_url + music
            time.sleep(5)
            yield Request(music_url, meta={'id': music_id}, callback=self.parse_music)

    # 获得音乐信息
    def parse_music(self, response):
        music_id = response.meta['id']
        music = response.xpath('//div[@class="tit"]/em[@class="f-ff2"]/text()').extract_first()
        artist = response.xpath('//div[@class="cnt"]/p[1]/span/a/text()').extract_first()
        album = response.xpath('//div[@class="cnt"]/p[2]/a/text()').extract_first()

        item = Cloud163Item()
        item['music'] = music
        item['id'] = music_id
        item['artist'] = artist
        item['album'] = album
        item['music_url'] = 'http://music.163.com/song/media/outer/url?id='+str(music_id)
        yield item
