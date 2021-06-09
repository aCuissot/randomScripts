import git
from unidiff import PatchSet
from datetime import date

from io import StringIO

repo_directory_address = "C:/Users/Axel/Documents/Github.io"

repository = git.Repo(repo_directory_address)
commit_sha1 = str(repository.rev_parse('master'))
print(commit_sha1)
commit = repository.commit(commit_sha1)

uni_diff_text = repository.git.diff(commit_sha1, commit_sha1 + '~1',
                                    ignore_blank_lines=True,
                                    ignore_space_at_eol=True)

patch_set = PatchSet(StringIO(uni_diff_text))

change_list = []  # list of changes
                  # [(file_name, [row_number_of_deleted_line],
                  # [row_number_of_added_lines]), ... ]

File = open("C:/Users/Axel/Documents/Github.io/Recent_changes", "a")

today = date.today()
# Textual month, day and year
d2 = today.strftime("%B %d, %Y")
File.write("<p>" + str(d2) + "</p><ul>")

for patched_file in patch_set:
    file_path = patched_file.path  # file name
    if file_path.split(".")[-1] not in ["jpg", "jpeg", "png", "mp3"]:
        print(file_path)
        number_of_lines = len(open(repo_directory_address + '/' + file_path, encoding="utf8").readlines())
        print('file name :' + file_path)
        del_line_no = [line.target_line_no
                       for hunk in patched_file for line in hunk
                       if line.is_added and
                       line.value.strip() != '']  # the row number of deleted lines
        print('deleted lines : ' + str(del_line_no))
        ad_line_no = [line.source_line_no for hunk in patched_file
                      for line in hunk if line.is_removed and
                      line.value.strip() != '']   # the row number of added liens
        print('added lines : ' + str(ad_line_no))
        change_list.append((file_path, del_line_no, ad_line_no))
        if len(ad_line_no) == number_of_lines:
            File.write("<li>Adding <a href=/" + file_path + ">" + file_path.split('/')[-1] + "</a></li>")
        elif (len(del_line_no) + len(ad_line_no))/number_of_lines > 0.3:
            File.write("<li>Modifying <a href=/" + file_path + ">" + file_path.split('/')[-1] + "</a></li>")

File.write("</ul><p> and minor changes </p>\n")

File.close()









