# JSON

[JSON开发笔记（一）—— JSON基础](https://www.jianshu.com/p/9afa65b49e49)

[JSON开发笔记（二）—— JSON Schema实战（上）](https://www.jianshu.com/p/2b7a2b1d0c49)

[JSON开发笔记（三）—— JSON Schema实战（中）](https://www.jianshu.com/p/9967edb199f5)

~~[JSON开发笔记（四）—— JSON Schema实战（下）](https://www.jianshu.com/p/eff366f76f69)  --java适用~~



# JSON Schema规范

JSON Schema是一种基于 JSON 格式定义 JSON 数据结构的规范，用于定义JSON数据结构以及校验JSON数据内容。JSON Schema官网地址：[http://json-schema.org/](https://link.jianshu.com/?t=http://json-schema.org/)

JSON 模式：

- 描述现有数据格式。
- 干净的人类和机器可读的文档。
- 完整的结构验证，有利于自动化测试。
- 完整的结构验证，可用于验证客户端提交的数据。



通过 JSON Schema 来校验录入的 JSON 数据的合法性

JSON Schema实际上就是一个JSON文件,  只不过其表示的信息内容是对另一个JSON文件结构和内容的约束



```json
{
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "Product",
    "description": "A product from Acme's catalog",
    "type": "object",
    "properties": {
        "id": {
            "description": "The unique identifier for a product",
            "type": "integer"
        },
        "name": {
            "description": "Name of the product",
            "type": "string"
        },
        "price": {
            "type": "number",
            "minimum": 0,
            "exclusiveMinimum": true
        }
    },
    "required": ["id", "name", "price"]
}
```





# JSON Schema关键字

要想完全理解上文中的JSON Schema文件内容，我们首先需要了解 JSON Schema 中关键字的含义和作用。JSON Schema中比较常见的关键字如下：

| 关键字           | 描述                                                         |
| ---------------- | ------------------------------------------------------------ |
| $schema          | 表示该JSON Schema文件遵循的规范                              |
| title            | 为该JSON Schema文件提供一个标题                              |
| description      | 关于该JSON Schema文件的描述信息                              |
| type             | 表示待校验元素的类型（例如，最外层的type表示待校验的是一个 JSON 对象，内层type分别表示待校验的元素类型为，整数，字符串，数字） |
| properties       | 定义待校验的 JSON 对象中，各个 key-value 对中 value 的限制条件 |
| required         | 定义待校验的 JSON 对象中，必须存在的 key                     |
| minimum          | 用于约束取值范围，表示取值范围应该大于或等于 minimum         |
| exclusiveMinimum | 如果 minimum 和 exclusiveMinimum 同时存在，且 exclusiveMinimum 的值为true，则表示取值范围只能大于 minimum |
| maximum          | 用于约束取值范围，表示取值范围应该小于或等于 maximum         |
| exclusiveMaximum | 如果 maximum 和 exclusiveMaximum 同时存在，且 exclusiveMaximum 的值为true，则表示取值范围只能小于 maximum |
| multipleOf       | 用于约束取值，表示取值必须能够被 multipleOf 所指定的值整除   |
| maxLength        | 字符串类型数据的最大长度                                     |
| minLength        | 字符串类型数据的最小长度                                     |
| pattern          | 使用正则表达式约束字符串类型数据                             |

其中，type的常见取值如下：

| type取值 | 对应 Java 数据类型            | 对应 python 数据类型 |
| -------- | ----------------------------- | -------------------- |
| array    | java.util.List                | list                 |
| boolean  | java.lang.Boolean             | bool                 |
| integer  | int（java.lang.Integer）      | int                  |
| number   | float（java.lang.Float）或int | float,  int          |
| null     | null                          | None                 |
| object   | java.lang.Object              | object               |
| string   | java.lang.String              | str                  |





# Json schema 类型

### object

```json
{
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "Product",
    "description": "A product from Acme's catalog",
    "type": "object",
    "properties": {
        "id": {
            "description": "The unique identifier for a product",
            "type": "integer"
        },
        "name": {
            "description": "Name of the product",
            "type": "string"
        },
        "price": {
            "type": "number",
            "minimum": 0,
            "exclusiveMinimum": true
        }
    },
    "required": ["id", "name", "price"]
}
```

object类型有三个关键字:

- type,  限定类型

- properties,  定义object的各个字段

- required,  限定必需字段

| 关键字               | 描述                    | 示例                                                         |
| -------------------- | ----------------------- | ------------------------------------------------------------ |
| type                 | 类型                    | .                                                            |
| properties           | 定义属性                |                                                              |
| required             | 必需属性                |                                                              |
| maxProperties        | 最大属性个数            |                                                              |
| minProperties        | 最小属性个数            |                                                              |
| additionalProperties | true or false or object | [参考](https://link.jianshu.com/?t=https://spacetelescope.github.io/understanding-json-schema/reference/object.html) |

properties 定义每个属性的名字和类型，方式如上例。



### array

```json
{
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "Product",
    "description": "A product from Acme's catalog",
    "type": "array",
    "items": {
        "type": "string"
     },
     "minItems": 1,
     "uniqueItems": true
}
```

array有三个单独的属性:  

- items

- minItems

- uniqueItems

| 关键字               | 描述                         | 示例                                                         |
| -------------------- | ---------------------------- | ------------------------------------------------------------ |
| items                | array 每个元素的类型         | .                                                            |
| minItems             | 约束属性，数组最小的元素个数 |                                                              |
| maxItems             | 约束属性，数组最大的元素个数 |                                                              |
| uniqueItems          | 约束属性，每个元素都不相同   |                                                              |
| additionalProperties | 约束items的类型，不建议使用  | [示例](https://link.jianshu.com/?t=https://spacetelescope.github.io/understanding-json-schema/reference/array.html) |
| Dependencies         | 属性依赖                     | [用法](https://link.jianshu.com/?t=https://spacetelescope.github.io/understanding-json-schema/reference/object.html?highlight=additionalproperties) |
| patternProperties    |                              | [用法](https://link.jianshu.com/?t=https://spacetelescope.github.io/understanding-json-schema/reference/object.html?highlight=patternproperties) |



### string

```json
{
   "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "Product",
    "description": "A product from Acme's catalog",
    "type": "object",
    "properties": {
        "ip": {
            "mail": "string",
            "pattern":"w+([-+.]w+)*@w+([-.]w+)*.w+([-.]w+)*"
        },
        "host": {
            "type": "phoneNumber",
            "pattern":"((d{3,4})|d{3,4}-)?d{7,8}(-d{3})*"
        },
    },
    "required": ["ip", "host"]
}
```

| 关键字    | 描述                      | 示例 |
| --------- | ------------------------- | ---- |
| maxLength | 定义字符串的最大长度，>=0 | .    |
| minLength | 定义字符串的最小长度，>=0 |      |
| pattern   | 用正则表达式约束字符串    |      |



### integer

```json
{
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "Product",
    "description": "A product from Acme's catalog",
    "type": "object",
    "properties": {
        "name": {
            "description": "Name of the product",
            "type": "string"
        },
        "price": {
            "type": "integer",
            "minimum": 0,
            "exclusiveMinimum": true
        }
    },
    "required": ["id", "name", "price"]
}
```

| 关键字           | 描述                                                         | 示例 |
| ---------------- | ------------------------------------------------------------ | ---- |
| minimum          | 最小值                                                       | .    |
| exclusiveMinimum | 如果存在 "exclusiveMinimum" 并且具有布尔值 true，如果它严格意义上大于 "minimum" 的值则实例有效。 |      |
| maximum          | 约束属性，最大值                                             |      |
| exclusiveMaximum | 如果存在 "exclusiveMinimum" 并且具有布尔值 true，如果它严格意义上小于 "maximum" 的值则实例有效。 |      |
| multipleOf       | 是某数的倍数，必须大于0的整数                                |      |



### number

```json
{
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "Product",
    "description": "A product from Acme's catalog",
    "type": "object",
    "properties": {
        "name": {
            "description": "Name of the product",
            "type": "string"
        },
        "price": {
            "type": "number",
            "minimum": 0,
            "exclusiveMinimum": true
        }
    },
    "required": ["id", "name", "price"]
}
```

number 关键字可以描述任意长度，任意小数点的数字。number类型的约束有以下几个：

| 关键字           | 描述                                                         | 示例 |
| ---------------- | ------------------------------------------------------------ | ---- |
| minimum          | 最小值                                                       | .    |
| exclusiveMinimum | 如果存在 "exclusiveMinimum" 并且具有布尔值 true，如果它严格意义上大于 "minimum" 的值则实例有效。 |      |
| maximum          | 约束属性，最大值                                             |      |
| exclusiveMaximum | 如果存在 "exclusiveMinimum" 并且具有布尔值 true，如果它严格意义上小于 "maximum" 的值则实例有效。 |      |



### boolean

```json
{
  "type": "object",
  "properties": {
    "number":      { "type": "boolean" },
    "street_name": { "type": "string" },
    "street_type": { "type": "string",
                     "enum": ["Street", "Avenue", "Boulevard"]
                   }
  }
}
```



### enum

```json
{
  "type": "object",
  "properties": {
    "number":      { "type": "number" },
    "street_name": { "type": "string" },
    "street_type": ["Street", "Avenue", "Boulevard"]                   
  }
}
```





# 进阶

### $ref

$ref 用来引用其它 schema

```json
{
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "Product set",
    "type": "array",
    "items": {
        "title": "Product",
        "type": "object",
        "properties": {
            "id": {
                "description": "The unique identifier for a product",
                "type": "number"
            },
            "name": {
                "type": "string"
            },
            "price": {
                "type": "number",
                "minimum": 0,
                "exclusiveMinimum": true
            },
            "tags": {
                "type": "array",
                "items": {
                    "type": "string"
                },
                "minItems": 1,
                "uniqueItems": true
            },
            "dimensions": {
                "type": "object",
                "properties": {
                    "length": {"type": "number"},
                    "width": {"type": "number"},
                    "height": {"type": "number"}
                },
                "required": ["length", "width", "height"]
            },
            "warehouseLocation": {
                "description": "Coordinates of the warehouse with the product",
                "$ref": "http://json-schema.org/geo"
            }
        },
        "required": ["id", "name", "price"]
    }
}
```



### definitions

当一个schema写的很大的时候，可能需要创建内部结构体，再使用$ref进行引用

```json
{
    "type": "array",
    "items": { "$ref": "#/definitions/positiveInteger" },
    "definitions": {
        "positiveInteger": {
            "type": "integer",
            "minimum": 0,
            "exclusiveMinimum": true
        }
    }
}
```



### allOf

```json
{
  "definitions": {
    "address": {
      "type": "object",
      "properties": {
        "street_address": { "type": "string" },
        "city":           { "type": "string" },
        "state":          { "type": "string" }
      },
      "required": ["street_address", "city", "state"]
    }
  },
 
  "allOf": [
    { "$ref": "#/definitions/address" },
    { "properties": {
        "type": { "enum": [ "residential", "business" ] }
      }
    }
  ]
}
```



### anyOf

```json
{
  "anyOf": [
    { "type": "string" },
    { "type": "number" }
  ]
}
```



### oneOf

```json
{
  "oneOf": [
    { "type": "number", "multipleOf": 5 },
    { "type": "number", "multipleOf": 3 }
  ]
}
```



### not

```json
{ "not": { "type": "string" } }
```







# 生成 JSON Schema

### 自动生成工具

##### json-schema-generator

```bash
pip install json-schema-generator
```



### 在线生成工具

根据JSON和对应的 JSON Schema 校验数据的正确性：[http://json-schema-validator.herokuapp.com/](https://link.jianshu.com?t=http://json-schema-validator.herokuapp.com/) 

根据JSON数据，生成对应的 JSON Schema 数据：[https://jsonschema.net/#/editor](https://link.jianshu.com?t=https://jsonschema.net/#/editor) 

根据JSON数据，生成对应的 JSON Schema 数据：[http://schemaguru.snowplowanalytics.com/#](https://link.jianshu.com?t=http://schemaguru.snowplowanalytics.com/#)





### python校验工具

##### jsonschema



##### fastjsonschema



##### json-schema-validator




# 校验 JSON Schema
https://github.com/Julian/jsonschema

https://github.com/zyga/json-schema-validator

fastjsonschema









# 高级用法记录

### dependencies

In the following example, whenever a `credit_card` property is provided, a `billing_address` property must also be present:

```
{
  "type": "object",

  "properties": {
    "name": { "type": "string" },
    "credit_card": { "type": "number" },
    "billing_address": { "type": "string" }
  },

  "required": ["name"],

  "dependencies": {
    "credit_card": ["billing_address"]
  }
}
```



### propertyNames

You might, for example, want to enforce that all names are valid ASCII tokens so they can be used as attributes in a particular programming language.

```
{
  "type": "object",
  "propertyNames": {
   "pattern": "^[A-Za-z_][A-Za-z0-9_]*$"
  }
}
```



### additionalProperties

The `additionalProperties` keyword is used to control the handling of extra stuff, that is, properties whose names are not listed in the `properties` keyword. By default any additional properties are allowed.

The `additionalProperties` keyword may be either a boolean or an object. If `additionalProperties` is a boolean and set to `false`, no additional properties will be allowed.

Reusing the example above, but this time setting `additionalProperties` to `false`.

```
{
  "type": "object",
  "properties": {
    "number":      { "type": "number" },
    "street_name": { "type": "string" },
    "street_type": { "type": "string",
                     "enum": ["Street", "Avenue", "Boulevard"]
                   }
  },
  "additionalProperties": false
}
```

If `additionalProperties` is an object, that object is a schema that will be used to validate any additional properties not listed in `properties`.

For example, one can allow additional properties, but only if they are each a string:

```
{
  "type": "object",
  "properties": {
    "number":      { "type": "number" },
    "street_name": { "type": "string" },
    "street_type": { "type": "string",
                     "enum": ["Street", "Avenue", "Boulevard"]
                   }
  },
  "additionalProperties": { "type": "string" }
}
```



### multipleOf

```
{
  "oneOf": [
    { "type": "number", "multipleOf": 5 },
    { "type": "number", "multipleOf": 3 }
  ]
}
```





# 自定义校验器

extend()

