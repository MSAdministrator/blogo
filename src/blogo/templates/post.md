title: {{ title }}
date: {{ date }}
draft: false
categories: [{%- for category in categories -%} "{{category}}", {%- endfor -%}]
tags: [{%- for category in categories -%} "{{category}}", {%- endfor -%}]
author: {{ author }}
