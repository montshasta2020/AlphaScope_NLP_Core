import os

import requests
from google.oauth2._credentials_async import UserAccessTokenCredentials
from google_auth_httplib2 import Request
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from allauth.socialaccount.models import SocialToken, SocialApp

from hello import unsplash
from hello.flaticon import FlatIconParser

"""
List of requests:
https://github.com/googleapis/google-api-python-client/blob/master/googleapiclient/discovery_cache/documents/slides.v1.json
"""


class Slideshow:

    def __init__(self, title, user, main_color=(0.192, 0.224, 0.302)):
        self.body = {"title": title}
        self.num_slides = 0
        self.num_elements = 0
        self.width = 720
        self.height = 405
        self.requests = []
        self.presentation_id = None
        self.user = user
        self.main_color = main_color
        self.main_color_a = (main_color[0], main_color[1], main_color[2], 1)
        self.flaticons = FlatIconParser(os.environ["FLATICON_KEY"])

    def add_slide(self):
        page_id = "zesavi_gpt3_slide_" + str(self.num_slides + 1)
        query = {
            "createSlide": {
                "objectId": page_id,
                "insertionIndex": str(self.num_slides),
                # 'slideLayoutReference': {
                #     'predefinedLayout': 'TITLE_AND_TWO_COLUMNS'
                # }
            }}
        self.num_slides += 1
        self.requests.append(query)
        return page_id

    """
    removes pages or elements
    """

    def remove_object(self, object_id):
        query = {
            "deleteObject": {
                "objectId": object_id
            }}
        self.requests.append(query)

    """
    Possible alignments: START, CENTER, END
    """

    def add_text(self, page_id, x, y, width, height, txt, size=14, color=None, font="Roboto", font_weight=400,
                 alignment="START", description=None):
        if color is None:
            color = self.main_color
        element_id = "element_" + str(self.num_elements)
        createShape = {
            'createShape': {
                'objectId': element_id,
                'shapeType': 'TEXT_BOX',
                'elementProperties': {
                    'pageObjectId': page_id,
                    'size': {
                        'height': {'magnitude': height, 'unit': 'PT'},
                        'width': {'magnitude': width, 'unit': 'PT'},
                    },
                    'transform': {
                        'scaleX': 1,
                        'scaleY': 1,
                        'translateX': x,
                        'translateY': y,
                        'unit': 'PT'
                    }
                }
            }
        }
        self.requests.append(createShape)
        insertText = {
            'insertText': {
                'objectId': element_id,
                'insertionIndex': 0,
                'text': txt if description is None else txt + "\n\n" + description["txt"]
            }
        }
        self.requests.append(insertText)
        updateTextStyle = {
            "updateTextStyle": {
                "objectId": element_id,
                "fields": "foregroundColor.opaqueColor.rgbColor,weightedFontFamily,fontSize",
                "style": {
                    "foregroundColor": {
                        "opaqueColor": {"rgbColor": {"red": color[0], "green": color[1], "blue": color[2]}}
                    },
                    "weightedFontFamily": {
                        "fontFamily": font,
                        "weight": font_weight
                    },
                    "fontSize": {'magnitude': size, 'unit': 'PT'}
                },
                "textRange": {
                    "type": "FIXED_RANGE",
                    "startIndex": 0,
                    "endIndex": len(txt),
                }
            }
        }
        self.requests.append(updateTextStyle)
        if description is not None:
            updateTextStyle = {
                "updateTextStyle": {
                    "objectId": element_id,
                    "fields": "fontSize",
                    "style": {
                        "fontSize": {'magnitude': 6, 'unit': 'PT'}
                    },
                    "textRange": {
                        "type": "FIXED_RANGE",
                        "startIndex": len(txt) + 1,
                        "endIndex": len(txt) + 2,
                    }
                }
            }
            self.requests.append(updateTextStyle)
            updateTextStyle = {
                "updateTextStyle": {
                    "objectId": element_id,
                    "fields": "foregroundColor.opaqueColor.rgbColor,weightedFontFamily,fontSize",
                    "style": {
                        "foregroundColor": {
                            "opaqueColor": {"rgbColor": {"red": description["color"][0],
                                                         "green": description["color"][1],
                                                         "blue": description["color"][2]}}
                        },
                        "weightedFontFamily": {
                            "fontFamily": description["font"],
                            "weight": description["font_weight"]
                        },
                        "fontSize": {'magnitude': description["size"], 'unit': 'PT'}
                    },
                    "textRange": {
                        "type": "FIXED_RANGE",
                        "startIndex": len(txt) + 2,
                        "endIndex": len(txt) + 2 + len(description["txt"]),
                    }
                }
            }
            self.requests.append(updateTextStyle)
        if alignment != "START":
            updateParagraphStyle = {
                "updateParagraphStyle": {
                    "objectId": element_id,
                    "fields": "alignment",
                    "style": {
                        "alignment": alignment
                    },
                    "textRange": {
                        "type": "ALL"
                    }
                }
            }
            self.requests.append(updateParagraphStyle)
        self.num_elements += 1
        return element_id

    """
    shadow cannot be set via API currently
    """

    def add_rectangle(self, page_id, x, y, width, height, fill_color, line_color=None):
        r, g, b, a = fill_color
        element_id = "element_" + str(self.num_elements)
        createShape = {
            'createShape': {
                'objectId': element_id,
                'shapeType': 'RECTANGLE',
                'elementProperties': {
                    'pageObjectId': page_id,
                    'size': {
                        'height': {'magnitude': height, 'unit': 'PT'},
                        'width': {'magnitude': width, 'unit': 'PT'},
                    },
                    'transform': {
                        'scaleX': 1,
                        'scaleY': 1,
                        'translateX': x,
                        'translateY': y,
                        'unit': 'PT'
                    }
                }
            }
        }
        updateProperties = {
            "updateShapeProperties": {
                "fields": "shapeBackgroundFill.solidFill,outline.propertyState" +
                          (",outline.solidFill" if line_color is not None else ""),
                "objectId": element_id,
                "shapeProperties": {
                    "shapeBackgroundFill": {
                        "solidFill": {"color": {"rgbColor": {"red": r, "green": g, "blue": b}}, "alpha": a}
                    },
                    # "shadow": {
                    #     "property_state": "RENDERED",
                    #     "alpha": 0.5,
                    #     "blur_radius": {'magnitude': 3, 'unit': 'PT'},
                    #     "color": {"rgbColor": {"red": 0, "green": 0, "blue": 0}},
                    #     "rotateWithShape": True,
                    #     "transform": {
                    #         'scaleX': 1,
                    #         'scaleY': 1,
                    #         'translateX': 0,
                    #         'translateY': 0,
                    #         'unit': 'PT'
                    #       }
                    # },
                    "outline": {
                        "property_state": "RENDERED" if line_color is not None else "NOT_RENDERED"
                    }
                }
            }
        }
        if line_color is not None:
            updateProperties["updateShapeProperties"]["shapeProperties"]["outline"]["solidFill"] = \
                {"color": {"rgbColor": {"red": line_color[0], "green": line_color[1], "blue": line_color[2]}},
                 "alpha": line_color[3]}
        self.requests.append(createShape)
        self.requests.append(updateProperties)
        self.num_elements += 1
        return element_id

    def add_image(self, page_id, x, y, width, height, url):
        element_id = "element_" + str(self.num_elements)
        req = {
            'createImage': {
                'objectId': element_id,
                'url': url,
                'elementProperties': {
                    'pageObjectId': page_id,
                    'size': {
                        'height': {'magnitude': height, 'unit': 'PT'},
                        'width': {'magnitude': width, 'unit': 'PT'}
                    },
                    'transform': {
                        'scaleX': 1,
                        'scaleY': 1,
                        'translateX': x,
                        'translateY': y,
                        'unit': 'PT'
                    }
                }
            }
        }
        self.requests.append(req)
        self.num_elements += 1
        return element_id

    """
    A point has a total width of 180 and height of 210
    """

    def generate_point(self, page_id, x, y, icon, title, text):
        desc = {
            "txt": text,
            "color": self.main_color,
            "font": "Roboto",
            "font_weight": 300,
            "size": 12
        }
        self.add_text(page_id, x + 10, y + 120, 160, 90, title, alignment="CENTER", description=desc)
        self.add_image(page_id, x + 40, y + 20, 100, 100, icon)

    def generate_slide_points_3(self, title, point1, point2, point3):
        page_id = self.add_slide()
        self.add_rectangle(page_id, 0, 0, 720, 95, self.main_color_a)
        self.add_text(page_id, 25, 40, 670, 40, title, size=28, color=(1, 1, 1), font_weight=300)
        self.generate_point(page_id, 80, 145, self.flaticons.find_best_match(point1["icon"])[0], point1["headline"],
                            point1["summary"])
        self.generate_point(page_id, 270, 145, self.flaticons.find_best_match(point2["icon"])[0], point2["headline"],
                            point2["summary"])
        self.generate_point(page_id, 460, 145, self.flaticons.find_best_match(point3["icon"])[0], point3["headline"],
                            point3["summary"])
        return page_id

    def generate_slide_points_2(self, title, point1, point2):
        page_id = self.add_slide()
        self.add_rectangle(page_id, 0, 0, 720, 95, self.main_color_a)
        self.add_text(page_id, 25, 40, 670, 40, title, size=28, color=(1, 1, 1), font_weight=300)
        self.generate_point(page_id, 170, 145, self.flaticons.find_best_match(point1["icon"])[0], point1["headline"],
                            point1["summary"])
        self.generate_point(page_id, 370, 145, self.flaticons.find_best_match(point2["icon"])[0], point2["headline"],
                            point2["summary"])
        return page_id

    def generate_slide_points_1(self, title, point1):
        page_id = self.add_slide()
        self.add_rectangle(page_id, 0, 0, 720, 95, self.main_color_a)
        self.add_text(page_id, 25, 40, 670, 40, title, size=28, color=(1, 1, 1), font_weight=300)
        self.generate_point(page_id, 270, 145, self.flaticons.find_best_match(point1["icon"])[0], point1["headline"],
                            point1["summary"])
        return page_id

    def generate_slide_points(self, slide_data):
        page_ids = []
        i = 0
        title = slide_data["title"]
        points = slide_data["points"]
        while len(slide_data["points"]) - i >= 5:
            page_ids.append(self.generate_slide_points_3(title, points[i], points[i + 1], points[i + 2]))
            i += 3
        if len(slide_data["points"]) - i == 4:
            page_ids.append(self.generate_slide_points_2(title, points[i], points[i + 1]))
            page_ids.append(self.generate_slide_points_2(title, points[i + 2], points[i + 3]))
        elif len(slide_data["points"]) - i == 3:
            page_ids.append(self.generate_slide_points_3(title, points[i], points[i + 1], points[i + 2]))
        elif len(slide_data["points"]) - i == 2:
            page_ids.append(self.generate_slide_points_2(title, points[i], points[i + 1]))
        elif len(slide_data["points"]) - i == 1:
            page_ids.append(self.generate_slide_points_1(title, points[i]))
        return page_ids

    def generate_slide_title(self, title, photo):
        page_id = self.add_slide()
        self.add_image(page_id, 0, 0, 720, 405, photo)
        self.add_text(page_id, 20, 130, 680, 60, title, 28, (1, 1, 1), alignment="CENTER")
        return page_id

    @staticmethod
    def from_json(user, data):
        slides = Slideshow(data["title"], user)
        slides.generate_slide_title(data["title"],
                                    unsplash.get_unsplash_image(data["photo"],
                                                                os.environ["UNSPLASH_KEY"], 1920, 1080)[0])
        for slide_data in data["slides"]:
            slides.generate_slide_points(slide_data)
        slides.remove_unknown_slides()
        slides.push()
        return slides

    def push(self):
        token = SocialToken.objects.get(account__user=self.user, account__provider='google')

        creds = Credentials(
            token=token.token,
            refresh_token=token.token_secret,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=os.environ["GOOGLE_CLIENT_ID"],
            client_secret=os.environ["GOOGLE_CLIENT_SECRET"])

        service = build('slides', 'v1', credentials=creds)
        if self.presentation_id is None:
            presentation = service.presentations().create(body=self.body).execute()
            self.presentation_id = presentation.get("presentationId")
            print("Created presentation with ID: {0}".format(presentation.get("presentationId")))
        response = service.presentations().batchUpdate(presentationId=self.presentation_id,
                                                       body={"requests": self.requests}).execute()
        self.requests.clear()

    def remove_unknown_slides(self):
        if self.presentation_id is None:
            self.push()
        token = SocialToken.objects.get(account__user=self.user, account__provider='google')
        creds = Credentials(
            token=token.token,
            refresh_token=token.token_secret,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=os.environ["GOOGLE_CLIENT_ID"],
            client_secret=os.environ["GOOGLE_CLIENT_SECRET"])
        service = build('slides', 'v1', credentials=creds)
        response = service.presentations().get(presentationId=self.presentation_id).execute()
        slides = response.get("slides")
        for s in slides:
            if not s["objectId"].startswith("zesavi_gpt3_slide_"):
                print(s["objectId"])
                self.remove_object(s["objectId"])

    def download(self):
        if self.presentation_id is None or len(self.requests) > 0:
            self.push()
        token = SocialToken.objects.get(account__user=self.user, account__provider='google')
        creds = Credentials(
            token=token.token,
            refresh_token=token.token_secret,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=os.environ["GOOGLE_CLIENT_ID"],
            client_secret=os.environ["GOOGLE_CLIENT_SECRET"])
        service = build('slides', 'v1', credentials=creds)
        urls = []
        for i in range(1, self.num_slides + 1):
            response = service.presentations().pages().getThumbnail(presentationId=self.presentation_id,
                                                                    pageObjectId="zesavi_gpt3_slide_" +
                                                                                 str(i)).execute()
            urls.append(response.get("contentUrl"))
        # width = response.get("width")
        # height = response.get("height")
        # print(url, width, height)
        return urls

    def get_url(self):
        if self.presentation_id is None:
            self.push()
        return "https://docs.google.com/presentation/d/" + self.presentation_id + "/"
