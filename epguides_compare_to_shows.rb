#!/usr/bin/env ruby

require 'net/http'
require 'uri'
require 'csv'

tvLocation = "/media/tv"
showTitle = "Trailer Park Boys"
url = "http://epguides.com/common/exportToCSV.asp?rage=6408" 
pageContent = Net::HTTP.get(URI.parse(url))

showCSV = pageContent.gsub!(/<.*?>/, "").gsub!(/^list output\s+$/, "").gsub!(/^\s+$/, "").gsub!(/^$\n/, "")

showStringArray = showCSV.split("\n")
headerArray = showStringArray.shift.split(",")
showHashArray = Array.new

showStringArray.each do |episode|
    # Simple split, doesn't really work if episode titles have commas...
    #tempEpisodeArray = episode.split(",")
    # Split regex to not split on commas inside quoted strings
    tempEpisodeArray = episode.split(/,(?!(?:[^",]|[^"],[^"])+")/)
    tempEpisodeHash = Hash.new

    headerArray.each_with_index do |column, index|
        tempEpisodeHash[column] = tempEpisodeArray[index]
    end

    tempEpisodeHash.delete("production code")
    tempEpisodeHash["title"].gsub!(/^"(.*?)"$/,'\1')

    tempEpisodeHash["file_name"] = "#{showTitle} - S"
    if tempEpisodeHash["season"].to_i < 10
        tempEpisodeHash["file_name"] += "0#{tempEpisodeHash["season"]}"
    else
        tempEpisodeHash["file_name"] += "#{tempEpisodeHash["season"]}"
    end
    if tempEpisodeHash["episode"].to_i < 10
        tempEpisodeHash["file_name"] += "E0#{tempEpisodeHash["episode"]}"
    else
        tempEpisodeHash["file_name"] += "E#{tempEpisodeHash["episode"]}"
    end
    # Put no file extension on the 'file_name' attribute' for matching below
    tempEpisodeHash["file_name"] += " - #{tempEpisodeHash["title"]}"

    showHashArray.push(tempEpisodeHash)
end

#puts "#{tvLocation}/#{showTitle}/Season #{showHashArray[0]["season"]}/#{showHashArray[0]["file_name"]}"

showHashArray.each_with_index do |ep, i|
    if File.exists?("#{tvLocation}/#{showTitle}/Season #{ep["season"]}/#{ep["file_name"]}.avi")\
    or File.exists?("#{tvLocation}/#{showTitle}/Season #{ep["season"]}/#{ep["file_name"]}.mkv")\
    or File.exists?("#{tvLocation}/#{showTitle}/Season #{ep["season"]}/#{ep["file_name"]}.mpg")\
    or File.exists?("#{tvLocation}/#{showTitle}/Season #{ep["season"]}/#{ep["file_name"]}.mp4")\
    or File.exists?("#{tvLocation}/#{showTitle}/Season #{ep["season"]}/#{ep["file_name"]}.m4v")
        #puts "Exists"
    else
        puts "#{tvLocation}/#{showTitle}/Season #{ep["season"]}/#{ep["file_name"]}"
    end
end
