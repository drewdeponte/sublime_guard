import sublime
import sublime_plugin
import thread
import subprocess
import os
import stat
import functools
import re

sublime_guard_controller = None


class GuardController(object):
    def __init__(self):
        self.proc = None
        self.running = False
        self.auto_show_enabled = True
        self.clear_when_find_this_text = None

    def set_listener(self, listener):
        self.listener = listener
        self.output_view = self.listener.window.get_output_panel('guard')
        self.enable_word_wrap()
        self.set_color_scheme()
        self.load_config()
        return self

    def open_file_paths(self):
        return [view.file_name() for view in self.listener.window.views() if view.file_name()]

    def open_folder_paths(self):
        return self.listener.window.folders()

    def path_has_guardfile(self, path):
        return os.path.exists(path + '/Guardfile')

    def find_project_root_path(self):
        project_root_path = None
        for path in self.open_folder_paths():
            print "Checking ... " + path
            if (self.path_has_guardfile(path)):
                project_root_path = path
                break
        return project_root_path

    def enable_word_wrap(self):
        self.output_view.settings().set("word_wrap", True)

    def set_color_scheme(self):
        self.output_view.settings().set("syntax", "Packages/Guard/GuardOutput.tmLanguage")
        self.output_view.settings().set("color_scheme", "Packages/Guard/GuardOutput.tmTheme")

    def enable_auto_show(self):
        self.auto_show_enabled = True

    def disable_auto_show(self):
        self.auto_show_enabled = False

    def set_permissions(self, path):
        os.chmod(path, stat.S_IRWXU | stat.S_IXGRP | stat.S_IRGRP | stat.S_IXOTH | stat.S_IROTH)

    def start_guard(self):
        project_root_path = self.find_project_root_path()
        if (project_root_path == None):
            sublime.error_message("Failed to find Guardfile in any of the open folders.")
        else:
            package_path = sublime.packages_path()
            self.set_permissions(package_path + "/Guard/guard_wrapper")
            self.set_permissions(package_path + "/Guard/run_guard.sh")
            cmd_array = [package_path + "/Guard/guard_wrapper", package_path + "/Guard/run_guard.sh", project_root_path]
            self.proc = subprocess.Popen(cmd_array, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.running = True
            self.show_guard_view_and_enable_autoshow()
            if self.proc.stdout:
                thread.start_new_thread(self.read_stdout, ())
            if self.proc.stderr:
                thread.start_new_thread(self.read_stderr, ())

    def read_stdout(self):
        while True:
            data = os.read(self.proc.stdout.fileno(), 2 ** 15)
            if data != "":
                sublime.set_timeout(functools.partial(self.append_data, data), 0)
            else:
                self.proc.stdout.close()
                self.running = False
                break

    def read_stderr(self):
        while True:
            data = os.read(self.proc.stderr.fileno(), 2 ** 15)
            if data != "":
                sublime.set_timeout(functools.partial(self.append_data, data), 0)
            else:
                self.proc.stderr.close()
                self.running = False
                break

    def append_data(self, data):
        if (self.auto_show_enabled):
            self.show_guard_view()
        clean_data = data.decode("utf-8")
        clean_data = self.normalize_line_endings(clean_data)
        clean_data = self.remove_terminal_color_codes(clean_data)

        # actually append the data
        self.output_view.set_read_only(False)
        edit = self.output_view.begin_edit()

        # clear the output window when a predefined text is found.
        if (self.clear_when_find_this_text and self.clear_when_find_this_text.search(clean_data)):
            self.output_view.erase(edit, sublime.Region(0, self.output_view.size()))

        self.output_view.insert(edit, self.output_view.size(), clean_data)

        # scroll to the end of the new insert
        self.scroll_to_end_of_guard_view()

        self.output_view.end_edit(edit)
        self.output_view.set_read_only(True)

    def normalize_line_endings(self, data):
        return data.replace('\r\n', '\n').replace('\r', '\n')

    def remove_terminal_color_codes(self, data):
        color_regex = re.compile("\\033\[[0-9;m]*", re.UNICODE)
        return color_regex.sub("", data)

    def scroll_to_end_of_guard_view(self):
        (cur_row, _) = self.output_view.rowcol(self.output_view.size())
        self.output_view.show(self.output_view.text_point(cur_row, 0))

    def show_guard_view_and_enable_autoshow(self):
        self.enable_auto_show()
        self.show_guard_view()

    def show_guard_view(self):
        self.listener.window.run_command('show_panel', {'panel': 'output.guard'})

    def hide_guard_view(self):
        self.disable_auto_show()
        self.listener.window.run_command('hide_panel', {'panel': 'output.guard'})

    def stop_guard(self):
        self.proc.stdin.write('e\n')
        self.proc.stdin.flush()
        self.running = False

    def is_guard_running(self):
        return self.running

    def reload_guard(self):
        self.proc.stdin.write('r\n')
        self.proc.stdin.flush()

    def run_all_tests(self):
        self.proc.stdin.write('\n')
        self.proc.stdin.flush()

    def output_help(self):
        self.proc.stdin.write('h\n')
        self.proc.stdin.flush()

    def toggle_notifications(self):
        self.proc.stdin.write('n\n')
        self.proc.stdin.flush()

    def pause(self):
        self.proc.stdin.write('p\n')
        self.proc.stdin.flush()

    def load_config(self):
        s = sublime.load_settings("Guard.sublime-settings")
        clear_text = s.get("clear_when_find_this_text")
        if (clear_text):
           self.clear_when_find_this_text = re.compile(clear_text)
        else:
           self.clear_when_find_this_text = None

def GuardControllerSingleton():
    global sublime_guard_controller
    if sublime_guard_controller == None:
        sublime_guard_controller = GuardController()
        return sublime_guard_controller
    else:
        return sublime_guard_controller


class StartGuardCommand(sublime_plugin.WindowCommand):

    def run(self):
        GuardControllerSingleton().set_listener(self).start_guard()

    def is_enabled(self):
        return not GuardControllerSingleton().is_guard_running()


class StopGuardCommand(sublime_plugin.WindowCommand):

    def run(self):
        GuardControllerSingleton().set_listener(self).stop_guard()

    def is_enabled(self):
        return GuardControllerSingleton().is_guard_running()


class HideGuardCommand(sublime_plugin.WindowCommand):

    def run(self):
        GuardControllerSingleton().set_listener(self).hide_guard_view()

    def is_enabled(self):
        return True


class ShowGuardCommand(sublime_plugin.WindowCommand):

    def run(self):
        GuardControllerSingleton().set_listener(self).show_guard_view_and_enable_autoshow()

    def is_enabled(self):
        return True


class ReloadGuardCommand(sublime_plugin.WindowCommand):

    def run(self):
        GuardControllerSingleton().set_listener(self).reload_guard()

    def is_enabled(self):
        return GuardControllerSingleton().is_guard_running()


class RunAllTestsGuardCommand(sublime_plugin.WindowCommand):

    def run(self):
        GuardControllerSingleton().set_listener(self).run_all_tests()

    def is_enabled(self):
        return GuardControllerSingleton().is_guard_running()


class RunAllTestsAndShowGuardCommand(sublime_plugin.WindowCommand):

    def run(self):
        GuardControllerSingleton().set_listener(self).show_guard_view()
        GuardControllerSingleton().set_listener(self).run_all_tests()


    def is_enabled(self):
        return GuardControllerSingleton().is_guard_running()


class OutputHelpGuardCommand(sublime_plugin.WindowCommand):

    def run(self):
        GuardControllerSingleton().set_listener(self).output_help()

    def is_enabled(self):
        return GuardControllerSingleton().is_guard_running()


class ToggleNotificationsGuardCommand(sublime_plugin.WindowCommand):

    def run(self):
        GuardControllerSingleton().set_listener(self).toggle_notifications()

    def is_enabled(self):
        return GuardControllerSingleton().is_guard_running()


class PauseGuardCommand(sublime_plugin.WindowCommand):

    def run(self):
        GuardControllerSingleton().set_listener(self).pause()

    def is_enabled(self):
        return GuardControllerSingleton().is_guard_running()
