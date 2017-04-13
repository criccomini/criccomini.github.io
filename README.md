Setup Repositories
============

    mkdir blog
    cd blog
    git clone git@github.com:criccomini/criccomini.github.io.git
    git clone git@github.com:criccomini/riccomini.name
    cd riccomini.name

Make Build Directory
============

    mkdir _site

Install Jekyll
============

    # make sure to install xcode command line tools first
    sudo gem install jekyll RedCloth

Run Jekyll
============

    jekyll serve

Shipping
============

    ./push

Liquid Information
============

Jekyll uses Liquid for templating. Here is some information that's useful when using Jekyll with Liquid templates:

* https://github.com/Shopify/liquid/wiki/Liquid-for-Designers
* http://en.wikipedia.org/wiki/Textile_(markup_language)
* https://github.com/mojombo/jekyll
* https://github.com/mojombo/jekyll/wiki/usage
* https://github.com/mojombo/jekyll/wiki/Sites
* https://github.com/mojombo/jekyll/wiki/YAML-Front-Matter
* https://github.com/mojombo/jekyll/wiki/Configuration
* https://github.com/mojombo/jekyll/wiki/Template-Data
