<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
        "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
    <title>FMl</title>
    <style>
        .author{
            font-style:italic;
        }
        li{
            list-style: none;
        }
        .picture, .message{
            float:left;
        }
    </style>
</head>
<body>


    <ul>
        % for post in data:
            %if 'message' in post:
                <li>
                    <div>
                        <div class="picture">
                            <img src="https://graph.facebook.com/{{ post['from']['id'] }}/picture" />

                        </div>
                        <div class="message">
                                            {{ post['message'] }} :   <span class="author">{{ post['from']['name'] }}</span>
                        </div>

                    </div>


                </li>
    </ul>


</body>
</html>