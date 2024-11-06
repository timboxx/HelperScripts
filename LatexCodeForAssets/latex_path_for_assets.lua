-- Lua script to generate LaTeX code for image inclusion
-- Usage: lua script.lua assets_folder

local lfs = require("lfs")  -- LuaFileSystem to iterate over files in a directory

-- Function to extract filename from a file path
function get_filename(path)
    return path:match("^.+/(.+)$") or path -- in case there's no directory in the path
end

-- Function to generate LaTeX code for each image
function generate_latex_for_image(filename)
    local tex_code = string.format([[
\begin{figure}[H]
    \centering
    \includegraphics[width=0.8\textwidth]{./assets/%s}
    \caption{%s}
\end{figure}

]], filename, filename:gsub("_", "\\_")) -- escape underscores in caption
    return tex_code
end

-- Check if the folder path is provided
if #arg < 1 then
    print("Please provide the path to the assets folder.")
    os.exit(1)
end

local folder_path = arg[1]

-- Start of the LaTeX document
local latex_document = [[
\documentclass{article}
\usepackage{graphicx}

\begin{document}

\section*{Plots and Responses}
]]

-- Iterate over all files in the given directory
for file in lfs.dir(folder_path) do
    -- Check if the file has a common image extension (adjust as needed)
    if file:match("%.png$") or file:match("%.jpg$") or file:match("%.jpeg$") or file:match("%.pdf$") then
        -- Generate LaTeX code for each image
        latex_document = latex_document .. generate_latex_for_image(file)
    end
end

-- End of the LaTeX document
latex_document = latex_document .. [[
\end{document}
]]

-- Print the LaTeX code
print(latex_document)
