class TemplateChoices:
    CLOUD_SERVER = "cloud_server"


class RenderTypeChoices:
    PDF = "PDF"
    CSV = "CSV"


class PlanSummaryChoices:
    CDN_DATA_TRANSFER = "cdn:data_transfer"
    S3_DATA_TRANSFER = "s3:data_transfer"
    S3_STORAGE = "s3:storage"
    S3_STORAGE_TRIAL = "s3:storage_trial"
    S3_DATA_TRANSFER_TRIAL = "s3:datatransfer_trial"
    S3_COLD = "s3:cold"
    S3_REQUEST = "s3:request"
    S3_STANDARD = "s3:standard"
