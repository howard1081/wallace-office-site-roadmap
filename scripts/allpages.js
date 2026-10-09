jQuery(document).ready(function($) {

    if(window.location.search.indexOf("page=mx-site-pages-add-new") != -1) {
        $('div#addNewPageDialog').fadeIn("fast");
    }

    $('a#addNewPage').click(function(){
        //  this just opens a dialog
        $('div#addNewPageDialog').fadeIn("fast");
        return false;
    });

    $('a#resetNavigation').click(function(){
        //  this just opens a dialog
        $('div#resetNavigationDialog').fadeIn("fast");
        return false;
    });

    $('div.mxRowActions a.mxDelete').click(function(){
        var id = $(this).closest('div.mxMoveableRow').attr('id').replace('nav', '');
        $('input#navKey').val(id);
        $('div#deletePage').fadeIn('fast');
        return false;
    });

    $('a#submitNewPage').click(function(){
    //
    //  The user's making a new page, so lets
    //  direct them to the right spot.
    //
        var val = $('div#addNewPageDialog select').val();
        switch(val){
            case 'blog':
                $(this).attr('href', $('input#site_url').val()+'/wp-admin/admin.php?page=mx-site-pages&mx-page=blog');
                break;
            case 'custom':
                $(this).attr('href', $('input#site_url').val()+'/wp-admin/post-new.php?post_type=page');
                break;
            case 'profile':
                $(this).attr('href', $('input#site_url').val()+'/wp-admin/admin.php?page=mx-site-pages&mx-page=profile');
                break;
            case 'property':
                $(this).attr('href', $('input#site_url').val()+'/wp-admin/admin.php?page=mx-site-pages&mx-page=property');
                break;
            case 'testimonial':
                $(this).attr('href', $('input#site_url').val()+'/wp-admin/admin.php?page=mx-site-pages&mx-page=testimonial');
                break;
            case 'testimonialtree':
                $(this).attr('href', $('input#site_url').val()+'/wp-admin/admin.php?page=mx-site-pages&mx-page=testimonial-tree');
                break;
            case 'moveeasy':
              $(this).attr('href', $('input#site_url').val()+'/wp-admin/admin.php?page=mx-site-pages&mx-page=move-easy');
              break;
            case 'menuitem':
                $(this).attr('href', $('input#site_url').val()+'/wp-admin/admin.php?page=mx-site-pages&mx-page=menuitem');
                break;
            case 'customsearch':
                $(this).attr('href', $('input#site_url').val()+'/wp-admin/admin.php?page=mx-site-pages&mx-page=customsearch');
                break;
            case 'menulink':
                $(this).attr('href', $('input#site_url').val()+'/wp-admin/admin.php?page=mx-site-pages&mx-page=menulink');
                break;
            case 'contactme':
                $(this).attr('href', $('input#site_url').val()+'/wp-admin/admin.php?page=mx-site-pages&mx-page=contactme');
                break;
            case 'homevalue':
                $(this).attr('href', $('input#site_url').val()+'/wp-admin/admin.php?page=mx-site-pages&mx-page=homevalue');
                break;
            case 'search':
            case 'financialcalculators':
            case 'equal-housing-opportunity':
            case 'homeupdate':
            case 'homepricingguide':
            case 'windermereblog':
            case 'buyingandselling':
            case 'windermerefoundation':
                $(this).attr('href', $('input#site_url').val()+'/wp-admin/admin.php?page=mx-site-pages&additem=' + val);
                break;
            default:
                $(this).attr('href', $('input#site_url').val()+'/wp-admin/admin.php?page=mx-appearance');
                break;
        }
        return true;
    });

    $('ol.mxSortable').nestedSortable({
            disableNestingClass: 'no-nest',
            forcePlaceholderSize: true,
            handle: 'div',
            helper: 'clone',
            items: 'li',
            listType: 'ol',
            opacity: .95,
            placeholder: 'mxPlaceholder',
            tabSize: 25,
            tolerance: 'pointer',
            isAllowed: function(item, parent) {
              if(item.hasClass("rootLevel") && parent != null) {
                var itmeMustBeRootLevel = true;
                return false;
              } else {
                var itmeMustBeRootLevel = false;
                return true;
              }
            },
            stop: function(event, ui) {
              if(itmeMustBeRootLevel) {
                alert("The page must stay at the root level!");
                var itmeMustBeRootLevel = false;
              } else {
                var isDirty = true;
              }
            },
            toleranceElement: '> div',
            cancel: 'li.mxNonMoveableRow > .mxMoveableRow'
    });

    $('ol.mxSortable').bind('sortstop', function(event, ui){
        $(this).stopSort();
    });

    var isIPad = (navigator.userAgent.match(/iPad/i) != null);
    if(isIPad){
      $('ol.mxSortable').draggable({
        cancel: 'li.mxNonMoveableRow'
      });
    }

    $('a#applyBulk').click(function(event){
        var bulkResult = $(this).applyBulk();
        // Post the form to save the changes to the show/hide rows
        if (true == bulkResult){
            $('input#publish').click();
        }
        return false;
    });

    $('a#applyBulkBottom').click(function(event){
        var bulkResult = $(this).applyBulk();
        // Post the form to save the changes to the show/hide rows
        if (true == bulkResult){
            $('input#publish').click();
        }
        return false;
    });

    $('a.mxShowHide').click(function (){
        $(this).setShowHide();
        // Post the form to save the changes to the show/hide rows
        $('input#publish').click();
        return false;
    });

    $('input#publish').click(function(e){
        var order = 1;
        $('ol.mxSortable > li > div.mxMoveableRow').each(function(){
            $(this).setValues(0, order);
            order++;
        });
        return true;
    });

    $('input.mxAllCheck').click(function(){
        if($(this).is(":checked")){
            $('input[type="checkbox"]').prop('checked', true);
        } else {
            $('input[type="checkbox"]').prop('checked', false);
        }
    });

    $('input[type="checkbox"]').click(function(){
        var masterList = $(this).parents('div.mxMoveableRow').siblings('ol,ul');  // we're gonna check or uncheck the inputs in this row
        if($(this).is(":checked")){
            masterList.find('input[type="checkbox"]').attr("checked", "checked");
        } else {
            masterList.find('input[type="checkbox"]').removeAttr("checked");
        }
    });

    jQuery.fn.applyBulk = function(parent, order){
    //================================================
    // The user's hit the apply bulk button, so lets
    // do what we need to apply the changes.
    //================================================
        var action = 'unknown';
        if (jQuery(this).attr('id').indexOf('Bottom') == -1)
            var action = jQuery('select#mxBulkTop').val();
        else
            var action = jQuery('select#mxBulkBottom').val();

        if('unknown' == action || 'Bulk Actions' == action){
            return false;
        }

        jQuery('div.mxMoveableRow').each(function(){
            var change;
            if(jQuery(this).find('input[type="checkbox"]').is(":checked")){
                change = true;
            } else {
                change = false;
            }
            if(action == 'Show' && change){
                jQuery(this).setShowHide('Show');
            }
            if(action == 'Hide' && change){
                jQuery(this).setShowHide('Hide');
            }
        });

        return true;
    };

    //================================================
    jQuery.fn.setValues = function(parent, order){
    //
    //  This function is called on each root level element in
    //  the navigation to set the hidden variables to update the
    //  page. It must recursively call itself in order to set the values
    //  for the children
    //
        //
        //  First, lets set the values for the element we are looping over.
        //
        var id = jQuery(this).attr('id').replace('nav', '');
        jQuery('input#order' + id).val(order);
        jQuery('input#parent' + id).val(parent);

        //
        //  Now that we have those set, lets check for a sibling ol/ul, which exists if
        //  there is a nested element
        //
        if(jQuery(this).siblings('ol,ul').length > 0){
            //
            //  We've got a nav, so lets loop over the children and call
            //  this same function recursively
            //
            //  Use the exact path to make sure we only collect the first level of navigation
            //
            var order = 1;
            jQuery(this).siblings('ol,ul').children('li').children('div.mxMoveableRow').each(function(){
                jQuery(this).setValues(id, order);
                order++;
            });

        }
    };

    jQuery.fn.setShowHideValues = function (setTo){
    //==========================================
    //  This function is called on an individual element
    //  and changes the values and markup appropriately
    //==========================================
        for (var i = 0; i < this.length; i++) {
            var jelm = jQuery(this[i]);
            var id = jelm.attr('id').replace('nav', '');
            jQuery('input#status'+id).val(setTo);
            jelm.find('a.mxShowHide').text(setTo == 'Show' ? 'Hide' : 'Show');
            setTo == 'Show' ? jelm.find('span').hide() : jelm.find('span').show();
        }
    };

    jQuery.fn.setShowHide = function (newVal){
    //
    //  This calls setShowHideValues on the correct elements.
    //  It's called on the div.moveableRow tag
    //
        var id = jQuery(this).closest('div.mxMoveableRow').attr('id').replace('nav', '');
        if(typeof newVal == 'undefined'){
            var oldVal = jQuery('input#status'+id).val();
            if('Show' == oldVal){
                var newVal = 'Hide';
            } else {
                var newVal = 'Show';
            }
        }

        if('Hide'==newVal){
            var alsochange = jQuery('div#nav'+id).siblings('ol,ul').find('div.mxMoveableRow');
        } else {
            var alsochange = jQuery(this).parent().parents('ol,ul').siblings('div.mxMoveableRow');
        }
        if(alsochange.length > 0){
            alsochange.setShowHideValues(newVal);
        }
        $('div#nav'+id).setShowHideValues(newVal);

        return false;
    };


    // BAF - Unfortunately we can't use the simple jQuery :even selector since it won't
    // correctly mark the nested rows.
/*
    jQuery.fn.resetZebra = function(){
        jQuery('ol.mxUlTable div.mxMoveableRow').parent().removeClass('mxAlternate');
        jQuery('ol.mxUlTable div.mxMoveableRow:even').parent().addClass('mxAlternate');
*/
    jQuery.fn.stopSort = function(){
    //=====================================================================
    //  We've stopped sorting, so lets check the table, such as
    //   1.  Make sure home is at the top.
    //=====================================================================
        if(jQuery('ol.mxUlTable li:first').attr('id') !== 'homepage'){
            var homerow = jQuery('li#homepage').detach();
            jQuery('ol.mxUlTable').prepend(homerow);
        }
        // Make sure we're only nested down to 3 levels
        var maxLevels = 3;
        var moreToQuery = true;
        var levelQuery = 'ol.mxUlTable > li';
        for (var i = 1; i <= maxLevels; i++)
            levelQuery += ' > ol > li';
        var query, parent, parentparent, cur;
        while (moreToQuery) {
            query = jQuery(levelQuery);
            moreToQuery = query.length > 0;
            if (moreToQuery)
                for (var j = 0; j < query.length; j++) {
                    cur = jQuery(query[j]);
                    parent = cur.parents('ul,ol');
                    if (parent.length > 1)
                        parent = jQuery(parent[0]);
                    parentparent = parent.parents('ol.mxUlTable ul,ol.mxUlTable ol');
                    if (parentparent.length > 0)
                        parentparent = jQuery(parentparent[0]);
                    else if (parentparent.length == 0)
                        parentparent = null; // This should never actually happen!
                    if (parent.length > 0 && parentparent) {
                        cur.detach();
                        parentparent.append(cur);
                    }
                }
        }
    }
});
