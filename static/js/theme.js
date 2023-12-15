/**
 * Theme: Xeloro - Admin & Dashboard Template
 * Author: Myra Studio
 * File: Main Js
 */


!function(t){"use strict";t("#side-menu").metisMenu(),t("#vertical-menu-btn").on("click",function(){t("body").toggleClass("enable-vertical-menu")}),t(".menu-overlay").on("click",function(){t("body").removeClass("enable-vertical-menu")}),t("#sidebar-menu a").each(function(){var a=window.location.href.split(/[?#]/)[0];this.href==a&&(t(this).addClass("active"),t(this).parent().addClass("mm-active"),t(this).parent().parent().addClass("mm-show"),t(this).parent().parent().prev().addClass("mm-active"),t(this).parent().parent().parent().addClass("mm-active"),t(this).parent().parent().parent().parent().addClass("mm-show"),t(this).parent().parent().parent().parent().parent().addClass("mm-active"))}),t(function(){t('[data-toggle="tooltip"]').tooltip()}),t(function(){t('[data-toggle="popover"]').popover()}),Waves.init()}(jQuery);