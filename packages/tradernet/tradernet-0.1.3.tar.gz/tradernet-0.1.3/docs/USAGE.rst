=====
Usage
=====

To use Tradernet API wrapper in a project::

    import tradernet as NtApi

    pub_ = 'Your Api key'
    sec_ = 'Your Api secret'

    res = NtApi.PublicApiClient(pub_, sec_, NtApi.PublicApiClient().V2)
    res.sendRequest(<команда>, <параметры>).content.decode("utf-8")

More details in `Tradernet official documentation <https://tradernet.com/tradernet-api/>`_.