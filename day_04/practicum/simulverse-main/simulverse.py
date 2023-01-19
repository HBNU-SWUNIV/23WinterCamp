import uvicorn
import sys

if __name__ == '__main__':
      if len(sys.argv) == 1:
            uvicorn.run("app.main:app",
                  host="0.0.0.0",
                  port=19612,
                  reload=True,
                  )
      elif sys.argv[1] == 'https':
            uvicorn.run("app.main:app",
                  host="0.0.0.0",
                  port=19612,
                  reload=True,
                  ssl_keyfile= '/home/cbchoi/ssl/cbchoi.info.key',
                  ssl_certfile= '/home/cbchoi/ssl/cbchoi.info.cer',
                  #workers=4
                  )
                  