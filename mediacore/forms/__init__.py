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

from tw import forms
from tw.forms import ListFieldSet, TextField, FileField, CalendarDatePicker, SingleSelectField, TextArea, Button, HiddenField, PasswordField
from tg.render import _get_tg_vars
from pylons.templating import pylons_globals
from mediacore.lib.helpers import line_break_xhtml


class LeniantValidationMixin(object):
    validator = forms.validators.Schema(
        allow_extra_fields=True, # Allow extra kwargs that tg likes to pass: pylons, start_request, environ...
    )

class SubmitButton(forms.SubmitButton):
    """Override the default SubmitButton validator.

    This allows us to have multiple submit buttons, or to have forms
    that are submitted without a submit button. The value for unclicked
    submit buttons will simply be C{None}.
    """
    validator = forms.validators.UnicodeString(if_missing=None)

class ResetButton(forms.ResetButton):
    validator = forms.validators.UnicodeString(if_missing=None)

class GlobalMixin(object):
    def display(self, *args, **kw):
        # Update the kwargs with the same values that are included in main templates
        # this allows us to access the following objects in widget templates:
        # ['tmpl_context', 'translator', 'session', 'ungettext', 'response', '_',
        #  'c', 'app_globals', 'g', 'url', 'h', 'request', 'helpers', 'N_', 'tg',
        #  'config']
        kw.update(_get_tg_vars())
        kw.update(pylons_globals())
        return forms.Widget.display(self, *args, **kw)

class Form(LeniantValidationMixin, GlobalMixin, forms.Form):
    pass

class ListForm(LeniantValidationMixin, GlobalMixin, forms.ListForm):
    pass

class TableForm(LeniantValidationMixin, GlobalMixin, forms.TableForm):
    pass

class CheckBoxList(GlobalMixin, forms.CheckBoxList):
    pass

class XHTMLTextArea(TextArea):
    def display(self, value=None, **kwargs):
        if value:
            value = line_break_xhtml(value)
        return TextArea.display(self, value, **kwargs)
