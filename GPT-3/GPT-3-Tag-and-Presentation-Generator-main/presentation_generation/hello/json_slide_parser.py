import json
import os

import openai


def make_valid_json(text):
    try:
        json_object = json.loads(text)
        return json_object
    except ValueError as e:
        # One quick fix that might work if we are lucky. Of course, thi needs more fancy fixing like in
        # https://ryanmarcus.github.io/dirty-json/
        print(text)
        text = text.rsplit('}', 1)[0] + "}]}]}"
        print(text)
        return json.loads(text)


def json_from_transcript(transcript):
    openai.api_key = os.environ["OPENAI_KEY"]
    prompt = "Input text: Hello everyone, today I want to talk to you about the charter of open AI. So one important " \
             "aspect are broadly distributed benefits. So we want artificial intelligence for the benefit of all. " \
             "While not enabling users of AI that may harm humanity. We also want to minimize conflicts of interests " \
             "among stakeholders that could compromise our goal. Apart from that, we want long term safety. So we " \
             "want you to research required to make artificial intelligence safe. And if a value aligned project " \
             "reaches the goal First, we are planning on teaming up with them in order to avoid the rights. In order " \
             "to achieve that, we also need technical leadership. So openly I must be on the cutting edge of AI " \
             "capabilities, and also lead with the pre products. Those should, in turn be used according to our " \
             "chart. Lastly, we have a cooperative orientation. So we want to actively cooperate with other research " \
             "and policy institutions to create a global community working together to address API's global " \
             "challenges, and provide public goods like source code.\nJSON: {\"title\":\"The Charter of OpenAI\"," \
             "\"photo\":\"contract\",\"slides\":[{\"title\":\"Broadly Distributed Benefits\",\"points\":[{" \
             "\"headline\":\"Benefit of all\",\"icon\":\"everyone\",\"summary\":\"Artificial Intelligence should be " \
             "for the benefit of all\"},{\"headline\":\"No harm\",\"icon\":\"harm\",\"summary\":\"No uses of AI that " \
             "enable harm to humanity should be enabled\"},{\"headline\":\"conflicts with stakeholders\"," \
             "\"icon\":\"stakeholder\",\"summary\":\"minimize conflicts of interest among stakeholders that could " \
             "compromise the goal\"}]},{\"title\":\"Long-Term Safety\",\"points\":[{\"headline\":\"Safety\"," \
             "\"icon\":\"safe\",\"summary\":\"Do research required to make artificial intelligence safe\"}," \
             "{\"headline\":\"Cooperation\",\"icon\":\"team\",\"summary\":\"if a value-aligned project reaches goal " \
             "first we are planning on teaming up with them\"}]},{\"title\":\"Technical Leadership\",\"points\":[{" \
             "\"headline\":\"Cutting Edge\",\"icon\":\"cutting edge\",\"summary\":\"OpenAI must be on cutting edge of " \
             "AI capabilities\"},{\"headline\":\"Preproducts\",\"icon\":\"product\",\"summary\":\"We must lead with " \
             "preproducts which should be used according to the charta\"}]},{\"title\":\"Cooperative Orientation\"," \
             "\"points\":[{\"headline\":\"Cooperation\",\"icon\":\"cooperation\",\"summary\":\"Actively cooperate " \
             "with other research and policy institutions\"},{\"headline\":\"Community\",\"icon\":\"community\"," \
             "\"summary\":\"Create a global community working together to address AGI's global challenges\"}," \
             "{\"headline\":\"Public Goods\",\"icon\":\"source code\",\"summary\":\"provide public goods like source " \
             "code\"}]}]}\nInput text: Hello, everyone. Welcome to this presentation of the MIT license. What is the " \
             "MIT license? It is a permissive free software license originating at the Massachusetts Institute of " \
             "Technology in the late 1980s is a permissive source license inputs only the limited restriction on " \
             "reuse and has therefore high license compatibility. In essence, it is compatible with many copyleft " \
             "licenses such as TGA mu. It can also be relicense as GPL software and integrated with either a GPL " \
             "software. It also permits. proprietary software provided at all copies of the license software include " \
             "a copy of the MIT license terms and copyright notice. MIT license software can also be relicensed as " \
             "proprietary software, which distinguishes it from copyleft software licenses. When talking about " \
             "popularity as of 2020, MIT was the most popular software license found in one analysis. Continuing from " \
             "reports in 2015 was the most popular software license on GitHub ahead of GPL and fo SS licenses, " \
             "not of a product that used an MIT license include the x Windows system, Ruby on Rails, nim, and others. " \
             "Compact notable components. Companies using the MIT license include Microsoft, Google and " \
             "Facebook.\nJSON: {\"title\":\"MIT License\",\"photo\":\"license\",\"slides\":[{\"title\":\"About\"," \
             "\"points\":[{\"headline\":\"Free software\",\"icon\":\"free\",\"summary\":\"Permissive free software " \
             "license\"},{\"headline\":\"MIT\",\"icon\":\"university\",\"summary\":\"Originating in MIT\"}," \
             "{\"headline\":\"Created in\",\"icon\":\"year\",\"summary\":\"Created in 1980s\"}]}," \
             "{\"title\":\"Compatibility\",\"points\":[{\"headline\":\"Copyleft compatibility\"," \
             "\"icon\":\"compatible\",\"summary\":\"The MIT License is compatible with many copyleft licenses, " \
             "such as GNU\"},{\"headline\":\"Proprietary SW\",\"icon\":\"software\",\"summary\":\"MIT License permits " \
             "reuse of proprietary software\"}]},{\"title\":\"Popularity\",\"points\":[{\"headline\":\"Most popular " \
             "2020\",\"icon\":\"popular\",\"summary\":\"As of 2020, MIT was the most popular software license found " \
             "in one analysis, continuing from reports of 2015\"},{\"headline\":\"Projects\",\"icon\":\"projects\"," \
             "\"summary\":\"Notable projects include the X Window System, Ruby on Rails, Nim\"}," \
             "{\"headline\":\"Companies\",\"icon\":\"companies\",\"summary\":\"Notable companies using the MIT " \
             "License include Microsoft, Facebook and Google\"}]}]}\nInput text: " \
             + transcript + "\nJSON:"
    print(prompt)
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        temperature=0.2,
        max_tokens=425,
        top_p=1.0,
        frequency_penalty=0.1,
        presence_penalty=0.0,
        stop=["\n"]
    )["choices"][0]["text"]
    print(response)
    return make_valid_json(response)
