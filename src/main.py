import utilities

def main():
    file = os.listdir(sys.argv[1])
    order_key = [int(re.findall('\d+', file[i])[0]) for i in range(len(file))]
    file = np.array(file)[np.array(order_key).argsort()]
    
    file_name = [sys.argv[1]+"/"+str(file[i]) for i in range(len(file))]

    global_nums = []
    global_aves = []

    for i in range(len(file)):
        picture = read_from_file(file_name[i])

        bi_picture = binarize_picture(picture, 195)  # 仅为相对阈值， 灰度强度为多少可以定义为晶粒不在讨论范围内, 但是一个固定的值才具有纵向比较的能力
        num, ave_area = count_grains(bi_picture, 8)  # 仅为相对大小， 面积达到多少可以记为晶粒不在讨论范围内
        global_nums.append(num)
        global_aves.append(ave_area)


    data = pd.DataFrame(global_nums, global_aves)
    data.to_excel('output.xlsx')
    


if __name__ == "__main__":
    main()

    
                
