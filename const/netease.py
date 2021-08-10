# -*- coding: UTF-8 -*-


class CompanyInfoXPath:
    type = "//table[@class='table_bg001 border_box limit_sale table_details']/tr[1]/td[2]/text()"
    region = "//table[@class='table_bg001 border_box limit_sale table_details']/tr[1]/td[4]/text()"
    short_name = "//table[@class='table_bg001 border_box limit_sale table_details']/tr[2]/td[2]/text()"
    address = "//table[@class='table_bg001 border_box limit_sale table_details']/tr[2]/td[4]/text()"
    full_name = "//table[@class='table_bg001 border_box limit_sale table_details']/tr[3]/td[2]/text()"
    telephone = "//table[@class='table_bg001 border_box limit_sale table_details']/tr[3]/td[4]/text()"
    english_name = "//table[@class='table_bg001 border_box limit_sale table_details']/tr[4]/td[2]/text()"
    email = "//table[@class='table_bg001 border_box limit_sale table_details']/tr[4]/td[4]/text()"
    capital = "//table[@class='table_bg001 border_box limit_sale table_details']/tr[5]/td[2]/text()"
    chairman = "//table[@class='table_bg001 border_box limit_sale table_details']/tr[5]/td[4]/text()"
    main_business = "//table[@class='table_bg001 border_box limit_sale table_details']/tr[10]/td[2]/text()"
    industry = "//div[@class='inner_box industry_info']/span[1]/em/a/text()"
