class GlobalValue:
    # FileType
    ImgsType = 'imgs'
    DocsType = 'docs'
    VideosType = 'videos'
    ProcedureType = 'Procedures'
    OthersType = 'others'

    FileTypes_choices = (
        (DocsType, DocsType),
        (ImgsType, ImgsType),
        (VideosType, VideosType),
        (ProcedureType, ProcedureType),
        (OthersType, OthersType),
    )

    ImgsSet = {'bmp', 'jpg', 'jpeg', 'png', 'tif', 'gif', 'pcx', 'tga', 'exif', 'fpx', 'svg', 'psd', 'cdr', 'pcd',
               'dxf', 'ufo', 'eps', 'ai', 'raw', 'WMF', 'webp'}

    DocsSet = {'txt', 'doc', 'ppt', 'md', 'xls', 'ppt', 'docx', 'xlsx', 'pptx', 'lrc', 'wps', 'zip', 'rar', '7z',
               'torrent', 'pdf'}

    VideoSet = {'mp4', 'mov', 'flv', 'avi', 'wmv', 'wav', 'mp3', 'cda', 'rm', 'rmvb', '3gp'}

    ProcedureSet = {'exe', 'py', 'java', 'cpp', 'js', 'jsx', 'tsx', 'class', 'pyc', 'app', 'apk', 'bat', 'html',
                    'css', 'sql', 'sqlite'}

    # Post infos
    PostFileLimitSize = 1024 * 1024 * 50  # 50MB
    PostFileLimitSizeError = 'File size over limitation of 50M'

    PostFileNameError = "File name can't empty"
    PostFileUrlError = "File url can't empty"

    # Post fields
    FileObj = 'file_obj'
    FileName = 'file_name'
    FileUrl = 'file_url'
    FileType = 'file_type'
    FileSize = 'file_size'
    FileUuid = 'file_uuid'
    FileVersion = 'file_version'
    FileNameHash = 'file_name_hash'
    FileDesc = 'file_desc'
    FIleCreateTime = 'create_at'

    # Email
    EmailFormatError = 'email format is error, should like xxx@xxx.com'
    UsernameError = 'the length of username should between 4 and  15'
    PasswordError = 'the length of username should between 4 and  15'
