definitions {
    script {
        type = "array"
        minItems =  1
        items {
            type = "object",
            oneOf = [
                {required = ["sh"]},
                {required = ["spark-submit"]}
            ]
            properties {
                sh {
                    type = "array"
                    minItems =  1
                    items {
                        type = "string"
                    }
                }
                spark-submit {
                    type = "object"
                    properties {
                        script {
                            type = "string"
                        }
                        conf {
                            type = "object"
                            additionalProperties {
                                type = "string"
                            }
                        }
                        settings {
                            type = "object"
                            additionalProperties {
                                type = "string"
                            }
                        }
                    }
                }
            }
        }
    }
    step {
        type = "object"
        propertyNames {
            pattern = "^[a-z0-9A-Z]([A-Za-z0-9\-\_\.]*[a-z0-9A-Z])?$"
            maxLength = 512
        }
        patternProperties {
            "^[a-z0-9A-Z]([A-Za-z0-9\-\_\.]*[a-z0-9A-Z])?$" {
                type = "object"
                required = ["image", "script"]
                properties {
                    image {
                        type = "string"
                    }
                    install {
                        type = "array"
                        items { type = "string" }
                    }
                    script { "$ref" = "#/definitions/script" }
                    resources {
                        type = "object"
                        properties {
                            cpu { type = "string" }
                            memory { type = "string" }
                            gpu { type = "string" }
                        }
                    }
                    retry {
                        type = "object"
                        required = ["limit"]
                        properties {
                            limit {
                                type = "integer"
                                minimum = 0
                                maximum = 5
                            }
                        }
                    }
                    depends_on  {
                        type = "array"
                        items { type = "string" }
                    }
                }
            }
        }
    }
}
title = "Span configuration schema v1.0"
type = "object"
required = ["version"]

anyOf = [
    {required = ["train"]},
    {required = ["serve"]},
    {required = ["batch_score"]},
]

properties "version" { type = "string" }

properties "train" {
    type = "object"
    oneOf = [
        {required = ["step"]},
        {required = ["image", "script"]}
    ]
    properties {
        step {
            oneOf = [
                { "$ref" = "#/definitions/step" },
                {
                    type = "array",
                    items { "$ref" = "#/definitions/step" }
                }
            ]
        }
        image {
            type = "string"
        }
        install {
            type = "array"
            items { type = "string" }
        }
        script { "$ref" = "#/definitions/script" }
        parameters {
            type = "object"
            additionalProperties {
                type = "string"
            }
        }
        secrets {
            type = "array"
            items { type = "string" }
        }
    }
}

properties "batch_score" {
    type = "object"
    oneOf = [
        {required = ["step"]},
        {required = ["image", "script"]}
    ]
    properties {
        step {
            oneOf = [
                { "$ref" = "#/definitions/step" },
                {
                    type = "array",
                    items { "$ref" = "#/definitions/step" }
                }
            ]
        }
        image {
            type = "string"
        }
        install {
            type = "array"
            items { type = "string" }
        }
        script { "$ref" = "#/definitions/script" }
        parameters {
            type = "object"
            additionalProperties {
                type = "string"
            }
        }
        secrets {
            type = "array"
            items { type = "string" }
        }
    }
}

properties "serve" {
    type = "object"
    required = ["image", "script"]
    properties {
        image {
            type = "string"
        }
        install {
            type = "array"
            items { type = "string" }
        }
        script {
            type = "array"
            minItems =  1
            items {
                type = "object"
                required = ["sh"]
                properties {
                    sh {
                        type = "array"
                        minItems =  1
                        items { type = "string" }
                    }
                }
            }
        }
    }
}
