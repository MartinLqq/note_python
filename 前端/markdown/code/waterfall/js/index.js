new Vue({
    el: '#app',
    props: {
        colNums: {
            type: Number,
            default () {
                return 6
            }
        },
        maxWidth: {
            type: Number,
            default() {
                // return window.innerWidth;
                return window.outerWidth;
                // return 600
            }
        },
        margin: {
            type: Number,
            default () {
                return 10
            }
        },
        images: {
            type: Array,
            default () {
                return [
                    'http://demo.htmleaf.com/1704/201704121503/img/set1/1.jpg',
                    'http://demo.htmleaf.com/1704/201704121503/img/set1/2.jpg',
                    'http://demo.htmleaf.com/1704/201704121503/img/set1/3.jpg',
                    'http://demo.htmleaf.com/1704/201704121503/img/set1/4.jpg',

                    'http://demo.htmleaf.com/1704/201704121503/img/set2/1.jpg',
                    'http://demo.htmleaf.com/1704/201704121503/img/set2/2.jpg',
                    'http://demo.htmleaf.com/1704/201704121503/img/set2/3.jpg',
                    'http://demo.htmleaf.com/1704/201704121503/img/set2/4.jpg',

                    'img/set3/1.jpg',
                    'img/set3/2.jpg',
                    'img/set3/3.jpg',
                    'img/set3/4.jpg',
                    'img/set3/5.jpg',
                    'img/set3/6.jpg',
                    'img/set3/7.jpg',
                    'img/set3/8.jpg',
                    'img/set3/9.jpg',
                    'img/set3/10.jpg',
                    'img/set3/11.jpg',
                ]
            }
        }
    },
    computed: {
        colWidth () {
            // 获取每一列的宽度
            const totalWidth = this.maxWidth - this.margin * this.colNums * 2
            let width = Math.floor(totalWidth / this.colNums)
            if (width < 1) width = 1
            return width
        }
    },
    mounted () {
        this.placeImages()
    },
    data: {
        loadCount: 0,
    },
    methods: {
        loadOne () {
            this.loadCount += 1
            if (this.loadCount === this.images.length) {
                // 图片全部加载完成, 在布局一次
                this.placeImages()
            }
        },
        placeImages() {
            const images = document.querySelectorAll('img')
            let colsHeight = []
            images.forEach((img, index, parent) => {
                if (index < this.colNums) {
                    // 布局第一行
                    colsHeight[index] = img.height + this.margin
                    img.style.position = 'absolute'
                    img.style.top = 0 + 'px'
                    img.style.left = this.colWidth * index + index * this.margin + 'px'
                } else {
                    // 第一行的图片都完成布局, 开始下一行

                    // 1.先找第一行的哪张图片高度最小
                    const minH = Math.min(...colsHeight)
                    const minIndex = colsHeight.indexOf(minH)

                    // 2.往这个高度最小的图片的下方布局一张图片
                    img.style.position = 'absolute'
                    img.style.top = colsHeight[minIndex] + 'px'
                    img.style.left = this.colWidth * minIndex + minIndex * this.margin + 'px'

                    // 3.更新高度的数组: 高度追加
                    colsHeight[minIndex] += img.height + this.margin
                }
            })
        }
    }
})
