# This file is a part of MediaCore, Copyright 2009 Simple Station Inc.
#
# MediaCore is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# MediaCore is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from tg.configuration import config
from routes import Mapper

def make_map():
    """Setup our custom named routes"""
    map = Mapper(directory=config['pylons.paths']['controllers'],
                 always_scan=config['debug'])

    #################
    # Public Routes #
    #################

    # Media list and non-specific actions
    # These are all mapped without any prefix to indicate the controller
    map.connect('/{action}',
        controller='media',
        action='index',
        requirements={'action': ('flow|upload|upload_submit|upload_success|'
                                 'upload_submit_async|upload_failure|index')})

    # Podcast list actions
    map.connect('/podcasts/feed/{slug}.xml',
        controller='podcasts',
        action='feed')
    map.connect('/podcasts/{slug}',
        controller='podcasts',
        action='view')

    # Category list actions
    map.connect('/tags/{slug}',
        controller='media',
        action='tags',
        slug=None)
    map.connect('/topics/{slug}',
        controller='media',
        action='topics',
        slug=None)

    # Individual media and actions their related actions
    map.connect('/view/{slug}/{action}',
        controller='media',
        action='view',
        requirements={'action': 'view|rate|comment'})
    map.connect('/files/{id}-{slug}.{type}',
        controller='media',
        action='serve',
        requirements={'id': r'\d+'})

    # Individual podcast media actions
    map.connect('/podcasts/{podcast_slug}/{slug}/{action}',
        controller='media',
        action='view',
        requirements={'action': 'view|rate|comment'})


    ################
    # Admin routes #
    ################

    map.connect('/admin/media_table/{table}/{page}',
        controller='admin',
        action='media_table')

    map.connect('/admin/media',
        controller='mediaadmin',
        action='index')
    map.connect('/admin/media/{id}/{action}',
        controller='mediaadmin',
        action='edit')

    map.connect('/admin/podcasts',
        controller='podcastadmin',
        action='index')
    map.connect('/admin/podcasts/{id}/{action}',
        controller='podcastadmin',
        action='edit')

    map.connect('/admin/comments',
        controller='commentadmin',
        action='index')
    map.connect('/admin/comments/{id}/{status}',
        controller='commentadmin',
        action='save_status',
        requirements={'status': 'approve|trash'})

    map.connect('/admin/settings',
        controller='settingadmin',
        action='index')

    map.connect('/admin/settings/config/{action}',
        controller='settingadmin',
        action='edit')

    map.connect('/admin/settings/users',
        controller='useradmin',
        action='index')
    map.connect('/admin/settings/users/{id}/{action}',
        controller='useradmin',
        action='edit')

    map.connect('/admin/settings/{category}',
        controller='categoryadmin',
        action='index',
        requirements={'category': 'topics|tags'})
    map.connect('/admin/settings/{category}/{id}/{action}',
        controller='categoryadmin',
        requirements={'category': 'topics|tags'})


    # Fallback Routes
    map.connect('/{controller}/{action}',
        action='index')

    # Set up object dispatch - this is required for TG's auth setup to work
    # FIXME: Look into this further...
    # Looks like routes.url_for doesn't work when using this route, so you
    # can't even switch back to routing. Argh.
    map.connect('*url',
        controller='root',
        action='routes_placeholder')

    return map
