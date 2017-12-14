import argparse
import os
import jira_access


def get_commit_msg(title, bugid):
    msg = ('[BugFix]' + title + '\n\n'
           '[id]:' + bugid + '\n'
           '[Products]\n'
           '    DORO 8040\n')
    return msg


def _git_commit(msg, is_quiet=True):
    cmd = "git commit -m " + msg
    if not is_quiet:
        cmd += " -e"
    os.system(cmd)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-b',
        '--bug_id',
        type=str,
        default='',
        help='Bug id. Default is current branch name'
    )

    parser.add_argument(
        '-m',
        '--manual_msg',
        action="store_true",
        default=False,
        help='Manually fill in git commit information.'
    )

    parser.add_argument(
        '-q',
        '--quiet',
        action="store_true",
        default=False,
        help='This option lets you further edit the git message.'
    )
    FLAGS, unparsed = parser.parse_known_args()

    # if FLAGS.bug_id == '':
    #     bug_id = os.popen('git rev-parse --abbrev-ref HEAD').readline().strip('\n')
    # else:
    #     bug_id = FLAGS.bug_id

    bug_id = (FLAGS.bug_id if FLAGS.bug_id else os.popen('git rev-parse --abbrev-ref HEAD').readline().strip('\n'))

    title = jira_access.get_title(bug_id)
    msg = get_commit_msg(title, bug_id)

    _git_commit(msg, FLAGS.quiet)








