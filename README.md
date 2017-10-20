# dpSpider

爬取地址：http://dpchallenge.com/

## 主文件 dp.py

运行获取图片存入 data/ ,信息存入 data.json.

### data.json图片信息解释

image_name---保存的图片名
image_url---图片源地址

information---图片摄影信息如下

    challenge--挑战
    
    collection--收藏
    
    camera--照相机
    
    lens--镜片

    aperture--光圈

    iso--感光度

    shutter--快门

    location--地点
    
    galleries--画廊(分类)
    
    date--拍摄时间
    
    date_uploaded--上传时间

    viewed--查看数

    comments--评论数

    favorites--最喜欢数

statistics---图片统计信息如下

    place--地点

    avg_all_users--所有用户平均分

    avg_commenters--评论者平均分
    
    avg_participants--参与者平均分

    avg_non_participants--非参与者平均分

    views_since_voting--投票以来意见

    views_during_voting--投票期间意见

    votes--投票数

    comments_num--评论数

    favorites--最喜欢数
    
comments---图片所有评论

