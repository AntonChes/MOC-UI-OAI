# OpenAI - MOC interface


### Setup | Config

First, create `.env` file. Use `.env.example` with all required envs and fill it:

- Add to your `.env` file user admin name (`ADMNAME`) and user password (`ADMPASS`);
- copy to env-file `API_KEY`s;
- as default, redis service will keep data *10 min* (**config.py -> REDIS_RECORD_TTL**);

### Setup | Docker usage

- **Build and up**

```sh
$ docker-compose build
.....
.....
$ docker-compose up -d
Recreating openai-moc-interface_web_1 ... done
```

- **Check the service running information**

```sh
$ docker-compose ps
           Name                 Command       State             Ports           
--------------------------------------------------------------------------------
openai-moc-interface_web_1   python main.py   Up      0.0.0.0:5000->5000/tcp,:::
                                                      5000->5000/tcp
```

- **stop the service**

```sh
$ docker-compose stop
Stopping openai-moc-interface_web_1 ... done
```

You should now be able to access the app at http://0.0.0.0:5000

### Routes

###### UI:
- **/**, index: with openai.Completion
- **/advanced**: with openai.ChatCompletion (GPT Turbo model)

###### API:
- **/api/chat-completion**
- **/api/health**
- **/api/dev/test_callback/<chat_id>** (for testing callback)
- **/tasks/<job_id>** (check Celery task by ID)

use Token for 3thd bot auth (**jwt.encode({'token': 'kinnekt-bot-auth-tok-001'}, 'GDtfDCFYjD', algorithm='HS256')**)

### Data

For now, for DEMO, we keep all info in json files in */data* folder.

This files contains info about products, for displayin Product Card in chat, static model pre-headers files, and info about 3thd party chat bots.