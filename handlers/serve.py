from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import blobstore


class ServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, resource):
        blob_info = blobstore.BlobInfo.get(resource)
        self.send_blob(blob_info)
