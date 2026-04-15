import httpx
import asyncio

BASE_URL = "http://localhost:5000"

async def test_api():
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        print("=" * 50)
        print("测试用户注册和登录")
        print("=" * 50)
        
        user_data = {
            "username": "testuser",
            "password": "testpass123",
            "full_name": "Test User"
        }
        
        print("\n1. 注册用户...")
        try:
            response = await client.post("/register", json=user_data)
            print(f"注册状态码: {response.status_code}")
            print(f"注册响应: {response.json()}")
        except Exception as e:
            print(f"注册失败: {e}")
        
        print("\n2. 登录用户...")
        try:
            login_data = {
                "username": "testuser",
                "password": "testpass123"
            }
            response = await client.post("/login", data=login_data)
            print(f"登录状态码: {response.status_code}")
            print(f"登录响应: {response.json()}")
            
            if response.status_code == 200:
                cookies = response.cookies
                print(f"获取到Cookie: {dict(cookies)}")
                
                print("\n3. 验证登录状态 (获取当前用户)...")
                response = await client.get("/users/whoami", cookies=cookies)
                print(f"获取用户状态码: {response.status_code}")
                print(f"当前用户: {response.json()}")
                
                print("\n" + "=" * 50)
                print("创建标签")
                print("=" * 50)
                
                tags = ["工作", "学习", "生活", "重要"]
                tag_ids = []
                
                for tag_name in tags:
                    print(f"\n创建标签: {tag_name}")
                    response = await client.post("/tags", json={"name": tag_name}, cookies=cookies)
                    print(f"状态码: {response.status_code}")
                    if response.status_code == 200:
                        tag_data = response.json()
                        print(f"创建成功: {tag_data}")
                        tag_ids.append(tag_data["id"])
                    else:
                        print(f"创建失败: {response.text}")
                
                print("\n" + "=" * 50)
                print("创建笔记")
                print("=" * 50)
                
                notes = [
                    {
                        "title": "Python学习笔记",
                        "content": "今天学习了Python的基础语法，包括变量、数据类型、条件语句和循环。Python是一门非常优雅的语言，缩进让代码更加整洁。",
                        "tags": [tag_ids[1], tag_ids[3]] if len(tag_ids) > 3 else []
                    },
                    {
                        "title": "工作计划",
                        "content": "下周需要完成的任务：\n1. 完成项目文档\n2. 代码审查\n3. 团队会议\n4. 客户演示",
                        "tags": [tag_ids[0], tag_ids[3]] if len(tag_ids) > 3 else []
                    },
                    {
                        "title": "周末计划",
                        "content": "这个周末打算：\n- 去公园散步\n- 看一部电影\n- 整理房间\n- 学习新技能",
                        "tags": [tag_ids[2]] if len(tag_ids) > 2 else []
                    },
                    {
                        "title": "FastAPI学习",
                        "content": "FastAPI是一个现代、快速的Web框架，基于Python类型提示。它自动生成API文档，性能非常好。",
                        "tags": [tag_ids[1]] if len(tag_ids) > 1 else []
                    }
                ]
                
                for note in notes:
                    print(f"\n创建笔记: {note['title']}")
                    response = await client.post("/notes", json=note, cookies=cookies)
                    print(f"状态码: {response.status_code}")
                    if response.status_code == 200:
                        print(f"创建成功: {response.json()}")
                    else:
                        print(f"创建失败: {response.text}")
                
                print("\n" + "=" * 50)
                print("获取所有笔记")
                print("=" * 50)
                
                response = await client.get("/notes", cookies=cookies)
                print(f"状态码: {response.status_code}")
                notes_data = response.json()
                print(f"共 {len(notes_data)} 条笔记")
                for note in notes_data:
                    print(f"\n- 标题: {note['title']}")
                    print(f"  作者: {note['author']['username']}")
                    if note.get('tags'):
                        print(f"  标签: {[t['name'] for t in note['tags']]}")
                
                if tag_ids:
                    print("\n" + "=" * 50)
                    print(f"按标签筛选笔记 (标签ID: {tag_ids[1]})")
                    print("=" * 50)
                    
                    response = await client.get(f"/notes?tag_id={tag_ids[1]}", cookies=cookies)
                    print(f"状态码: {response.status_code}")
                    filtered_notes = response.json()
                    print(f"筛选后共 {len(filtered_notes)} 条笔记")
                    for note in filtered_notes:
                        print(f"\n- 标题: {note['title']}")
                
                print("\n" + "=" * 50)
                print("测试完成！")
                print("=" * 50)
                print("\n您可以访问 http://localhost:8080 来查看应用")
                print(f"登录账号: testuser")
                print(f"登录密码: testpass123")
                
        except Exception as e:
            print(f"登录失败: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_api())
