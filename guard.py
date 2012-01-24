import sublime
import sublime_plugin
import thread
import subprocess
import os
import functools


# TODO: make it so that there is a way to start guard
# TODO: make it so there is a way to show the guard panel
# TODO: make it so there is a way to hide the guard panel
# TODO: make it so there is a way to stop the previously started guard process

sublime_guard_controller = None


class GuardController(object):
    def __init__(self, listener):
        self.proc = None
        self.running = False
        self.listener = listener
        self.output_view = self.listener.window.get_output_panel('guard')

    def start_guard(self):
        self.proc = subprocess.Popen(['/Users/adeponte/bin/wrap_guard'], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.running = True
        self.show_guard_view()
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
        clean_data = data.decode("utf-8")
        clean_data = clean_data.replace('\r\n', '\n').replace('\r', '\n')

        self.output_view.set_read_only(False)
        edit = self.output_view.begin_edit()
        self.output_view.insert(edit, self.output_view.size(), clean_data)

        # scroll to the end of the new insert
        self.output_view.show(self.output_view.size())

        self.output_view.end_edit(edit)
        self.output_view.set_read_only(True)

    def show_guard_view(self):
        self.listener.window.run_command('show_panel', {'panel': 'output.guard'})

    def hide_guard_view(self):
        self.listener.window.run_command('hide_panel', {'panel': 'output.guard'})

    def stop_guard(self):
        self.proc.terminate()
        self.running = False

    def is_guard_running(self):
        return self.running


def GuardControllerSingleton(listener):
    global sublime_guard_controller
    if sublime_guard_controller == None:
        sublime_guard_controller = GuardController(listener)
        return sublime_guard_controller
    else:
        return sublime_guard_controller


class StartGuardCommand(sublime_plugin.WindowCommand):

    def run(self):
        GuardControllerSingleton(self).start_guard()

    def is_enabled(self):
        return not GuardControllerSingleton(self).is_guard_running()


class StopGuardCommand(sublime_plugin.WindowCommand):

    def run(self):
        GuardControllerSingleton(self).stop_guard()

    def is_enabled(self):
        return GuardControllerSingleton(self).is_guard_running()


class HideGuardCommand(sublime_plugin.WindowCommand):

    def run(self):
        GuardControllerSingleton(self).hide_guard_view()

    def is_enabled(self):
        return True


class ShowGuardCommand(sublime_plugin.WindowCommand):

    def run(self):
        GuardControllerSingleton(self).show_guard_view()

    def is_enabled(self):
        return True
