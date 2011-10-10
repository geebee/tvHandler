#!/usr/bin/env ruby

def parseShowToHash(showTitle = "")
    raise ArgumentError, "showTitle is a required parameter" if showTitle.empty?

    require 'rubygems'
    require 'nokogiri'
    require 'open-uri'
    require 'htmlentities'

    epguidesTitle = showTitle.split(" ").join()
    epguidesURL = "http://epguides.com/#{epguidesTitle}/"

    escapeHtmlEntities = HTMLEntities.new
    preShowPage = Nokogiri::HTML(open(epguidesURL)).to_html.gsub!("\n","")
    showPage = escapeHtmlEntities.decode(preShowPage)
    showHashArray = Array.new

    #puts "---------"
    #puts showPage
    #puts "---------"
    
    #showPage.scan(/\d+. +(\d+) *\- *(\d+).*?<a.*?>(.*?)<\/a>/) do |season, episode, title|
    showPage.scan(/[\d]+[\s]+([\d]+)\-([\d]+).*?([0-9]{2}\/[a-zA-Z]{3}\/[0-9]{2,4}|UNAIRED)[\s]+<a.*?>(.*?)<\/a>/) do |season, episode, airDate, title|
        #puts "Season: #{season}, Episode: #{episode} - Title: #{title} (Aired: #{airDate})"
        tempEpisodeHash = Hash.new

        tempEpisodeHash[:season] = season
        tempEpisodeHash[:episode] = episode
        tempEpisodeHash[:airDate] = airDate
        tempEpisodeHash[:title] = title.gsub("\"", "") 

        tempEpisodeHash[:fileName] = "#{showTitle} - S"
        if tempEpisodeHash[:season].to_i < 10
            tempEpisodeHash[:fileName] += "0#{tempEpisodeHash[:season]}"
        else
            tempEpisodeHash[:fileName] += "#{tempEpisodeHash[:season]}"
        end
        
        tempEpisodeHash[:fileName] += "E#{tempEpisodeHash[:episode]}"
        #
        # Put no file extension on the 'fileName' attribute' for matching below
        tempEpisodeHash[:fileName] += " - #{tempEpisodeHash[:title]}"

        showHashArray.push(tempEpisodeHash)
    end
    
    return showHashArray
end


def compareShowHashToExisting(showHashArray = Hash.new, showTitle = "", tvLocation = "")
    # Trusty fall-back of a working debug message...
    # puts "#{tvLocation}/#{showTitle}/Season #{showHashArray[0][:season]}/#{showHashArray[0][:fileName]}"

    raise ArgumentError, "showHashArray is a required parameter" if showHashArray.empty?
    raise ArgumentError, "showTitle is a required parameter" if showTitle.empty?
    raise ArgumentError, "tvLocation is a required parameter" if tvLocation.empty?

    require 'date'

    puts "Out of #{showHashArray.length} Episodes in: #{showTitle}..."

    matchingEpisodes = 0
    missingAndAired = 0
    unairedEpisodes = 0
    
    showHashArray.each_with_index do |ep, i|
        if File.exists?("#{tvLocation}/#{showTitle}/Season #{ep[:season]}/#{ep[:fileName]}.avi")\
        or File.exists?("#{tvLocation}/#{showTitle}/Season #{ep[:season]}/#{ep[:fileName]}.mkv")\
        or File.exists?("#{tvLocation}/#{showTitle}/Season #{ep[:season]}/#{ep[:fileName]}.mpg")\
        or File.exists?("#{tvLocation}/#{showTitle}/Season #{ep[:season]}/#{ep[:fileName]}.mp4")\
        or File.exists?("#{tvLocation}/#{showTitle}/Season #{ep[:season]}/#{ep[:fileName]}.m4v")
            #puts "Exists"
            matchingEpisodes += 1
        else
            if ep[:airDate] == "UNAIRED"
                unairedEpisodes += 1
                break
            end
            # If the episode has already aired...
            if Date.strptime(Time.now.strftime("%d/%b/%y"), "%d/%b/%y") > Date.strptime("#{ep[:airDate]}", "%d/%b/%y")
                missingAndAired += 1
                puts ".....Missing Aired Episode: #{ep[:fileName]}"
            else
                unairedEpisodes += 1
                puts ".....Missing Unaired Episode: #{ep[:fileName]}"
            end
        end
    end

    puts "...#{matchingEpisodes} Match as expected."
    puts "...#{missingAndAired} Have aired, but are not found"
    puts "...#{unairedEpisodes} Are scheduled, but have not aired."
end

require 'optparse'

options = {}

optparse = OptionParser.new do |opts|
    opts.banner = "Usage: ./epguides_compare_to_shows.rb --tv-folder/-f <directory> --title/-t <show title> ..."

    options[:folder] = "/media/tv"
    opts.on("-f", "--tv-folder FOLDER", "Top-Level directory containing the shows to compare") do |folder|
        options[:folder] = folder
    end

    options[:title] = ""
    opts.on("-t", "--title TITLE", "Title of the show to compare") do |title|
        options[:title] = title
    end

    opts.on("-h", "--help", "Display this help screen") do
        puts opts
        exit
    end
end

optparse.parse!

tvLocation = "#{options[:folder]}"
showTitle = "#{options[:title]}"

if showTitle == ""
    puts "-t/--title <show title> is a required parameter."
    exit
end

puts "Using Directory: #{tvLocation}"
puts "Show Title: #{showTitle}"

showsToCheck = ["30 Rock", "Alias", "Arrested Development"]
# TODO: In future, iterate this array to make the hash of shows to parse, etc...

shows = Hash.new

shows["#{showTitle}"] = parseShowToHash(showTitle)
compareShowHashToExisting(shows["#{showTitle}"], showTitle, tvLocation)
