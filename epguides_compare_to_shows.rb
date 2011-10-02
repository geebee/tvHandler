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
    tempEpisodeArray = episode.split(",")
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
    tempEpisodeHash["file_name"] += " - #{tempEpisodeHash["title"]}.avi"

    showHashArray.push(tempEpisodeHash)
end

puts "#{tvLocation}/#{showTitle}/Season #{showHashArray[0]["season"]}/#{showHashArray[0]["file_name"]}"
