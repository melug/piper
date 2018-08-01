# Piper

Piper is light-weight crawling tool which is inspired by [Unix pipelines](https://en.wikipedia.org/wiki/Pipeline_(Unix)).

Piper is built around the idea that sees web pages or resources on the internet flowing through the series of command. Each command is supposed to process the information such as parsing html or extracting the links. 

## Concepts

Piece of information that flows through the command is called [Resource](https://github.com/melug/piper/blob/master/piper/base.py#L6) meaning that resource on the internet. Resource contains following attributes:

* Request
* Response
* Session. These three objects are directly taken from [requests](http://docs.python-requests.org/en/master/) framework. 
* Meta. This is where we save custom information like download date, parsed html, extracted text and basically anything you can think of.

Since the idea of resource is very abstract, we can see that each command takes resources and returns several resources. 

The command concept in Piper is called [Processor](https://github.com/melug/piper/blob/master/piper/base.py#L9). Since Processor takes resources and returns resources, we should be able to combine existing processors.

The library already defined some basic processors. Some of them are:

* Download. Downloads resources
* ParseHtml. Parses resource response and save parsed html in meta
* ExtractText. Extracts text from parsed html

## Example

.. code-block:: python

    from piper.base import Download
    from piper.http import ContentTypeFilter
    from piper.html import ParseHtml
    
    download_and_parse_html = Download() | ContentTypeFilter("text/html") | ParseHtml()
    

The newly built `download_and_parse_html` command downloads the given request and filters based content type header. In this case, header should be "text/html" then at last it parses html then saves it.

Real adventure doesn't end there. You use this command with combination other processors again. For example:

.. code-block:: python
    
    from piper.html import ExtractElement
    
    download_new_links = download_and_parse_html | ExtractElement("a") | download_and_parse_html

This new command uses previous command's result to extract links and then downloads those new pages and parses. See [examples](https://github.com/melug/piper/tree/master/examples).

## Installation

Download the repo and run

.. code-block: text

    python setup.py install
    
Piper supports python 3.6 and above.
