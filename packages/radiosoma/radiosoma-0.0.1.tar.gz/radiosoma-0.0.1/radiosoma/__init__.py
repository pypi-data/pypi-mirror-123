import requests
from ovos_utils.xml_helper import xml2dict


class SomaFmStation:
    def __init__(self, raw):
        self.raw = raw

    @property
    def station_id(self):
        return self.raw.get("id")

    @property
    def title(self):
        return self.raw.get("title") or self.raw.get("id")

    @property
    def image(self):
        return self.raw.get("xlimage") or \
               self.raw.get("largeimage") or \
               self.raw.get("image")

    @property
    def description(self):
        return self.raw.get("description", "")

    @property
    def genre(self):
        return self.raw.get("genre")

    @property
    def streams(self):
        streams = []
        for stream in self.raw.get("fastpls", []):
            try:
                streams.append(stream["text"])
            except:
                continue
        for stream in self.raw.get("highestpls", []):
            try:
                streams.append(stream["text"])
            except:
                continue
        return streams

    @property
    def best_stream(self):
        for stream in self.raw.get("highestpls", []):
            try:
                return stream["text"]
            except:
                continue
        for stream in self.raw.get("fastpls", []):
            try:
                return stream["text"]
            except:
                continue

    @property
    def fastest_stream(self):
        for stream in self.raw.get("fastpls", []):
            try:
                return stream["text"]
            except:
                continue
        for stream in self.raw.get("highestpls", []):
            try:
                return stream["text"]
            except:
                continue

    @property
    def m3u_stream(self):
        return f"http://somafm.com/m3u/{self.station_id}.m3u"

    @property
    def direct_stream(self):
        return f"http://ice2.somafm.com/{self.station_id}-128-mp3"

    @property
    def alt_direct_stream(self):
        return f"http://ice4.somafm.com/{self.station_id}-128-mp3"

    def __str__(self):
        return self.fastest_stream

    def __repr__(self):
        return self.title + ":" + str(self)


def get_stations():
    xml = requests.get("http://api.somafm.com/channels.xml").text
    for channel in xml2dict(xml)["channels"]["channel"]:
        yield SomaFmStation(channel)
